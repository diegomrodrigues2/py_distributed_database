import os
import sys
import tempfile
import unittest
import time
import grpc

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.replication.replica.grpc_server import NodeServer, ReplicaService
from database.replication.replica import replication_pb2, replication_pb2_grpc
from database.utils.vector_clock import VectorClock


class ReplicaServiceTimestampTest(unittest.TestCase):
    def test_put_delete_respects_timestamps(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            node = NodeServer(db_path=tmpdir)
            service = ReplicaService(node)

            # existing value with newer timestamp
            node.db.put("k", "v1", timestamp=10)

            # update with older timestamp should be ignored
            req_old = replication_pb2.KeyValue(key="k", value="old", timestamp=5)
            service.Put(req_old, None)
            self.assertEqual(node.db.get("k"), "v1")

            # update with newer timestamp should overwrite
            req_new = replication_pb2.KeyValue(key="k", value="new", timestamp=20)
            service.Put(req_new, None)
            self.assertEqual(node.db.get("k"), "new")

            # prepare record for delete tests
            node.db.put("d", "val", timestamp=15)

            # node clock small -> delete ignored
            node.clock.time = 0
            service.Delete(replication_pb2.KeyRequest(key="d", timestamp=0, node_id="test"), None)
            self.assertEqual(node.db.get("d"), "val")

            # node clock high -> delete applied
            node.clock.time = 100
            service.Delete(replication_pb2.KeyRequest(key="d", timestamp=200, node_id="test"), None)
            self.assertIsNone(node.db.get("d"))

            node.db.close()


class ReplicaServiceSequenceTest(unittest.TestCase):
    def test_sequence_number_prevents_duplicates(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            node = NodeServer(db_path=tmpdir)
            service = ReplicaService(node)

            req1 = replication_pb2.KeyValue(
                key="k",
                value="v1",
                timestamp=10,
                node_id="node_b",
                op_id="node_b:1",
            )
            service.Put(req1, None)
            self.assertEqual(node.db.get("k"), "v1")

            # duplicate with same sequence should be ignored
            dup = replication_pb2.KeyValue(
                key="k",
                value="v2",
                timestamp=20,
                node_id="node_b",
                op_id="node_b:1",
            )
            service.Put(dup, None)
            self.assertEqual(node.db.get("k"), "v1")

            # higher sequence should be applied
            req2 = replication_pb2.KeyValue(
                key="k",
                value="v2",
                timestamp=20,
                node_id="node_b",
                op_id="node_b:2",
            )
            service.Put(req2, None)
            self.assertEqual(node.db.get("k"), "v2")

            node.db.close()


class FetchUpdatesTest(unittest.TestCase):
    def test_fetch_updates_apply_and_return(self):
        with tempfile.TemporaryDirectory() as dir_a, tempfile.TemporaryDirectory() as dir_b:
            node_a = NodeServer(db_path=dir_a, node_id="A")
            node_b = NodeServer(db_path=dir_b, node_id="B")
            service_a = ReplicaService(node_a)

            # Operation from node B to be applied on node A
            op_b = replication_pb2.Operation(
                key="k1",
                value="v1",
                timestamp=1,
                node_id="B",
                op_id="B:1",
                delete=False,
            )

            # Node A has a pending operation to send back
            node_a.replication_log["A:1"] = ("k2", "v2", 2)

            req = replication_pb2.FetchRequest(
                vector=replication_pb2.VersionVector(items={}),
                ops=[op_b],
            )

            resp = service_a.FetchUpdates(req, None)

            self.assertEqual(node_a.db.get("k1"), "v1")
            self.assertEqual(len(resp.ops), 1)
            self.assertEqual(resp.ops[0].key, "k2")
            self.assertEqual(resp.ops[0].op_id, "A:1")

            node_a.db.close()
            node_b.db.close()


class AntiEntropyLoopTest(unittest.TestCase):
    def test_anti_entropy_loop_syncs_nodes(self):
        with tempfile.TemporaryDirectory() as dir_a, tempfile.TemporaryDirectory() as dir_b:
            node_a = NodeServer(db_path=dir_a, node_id="A", peers=[])
            node_b = NodeServer(db_path=dir_b, node_id="B", peers=[])
            service_b = ReplicaService(node_b)

            node_b.replication_log["B:1"] = ("k", "v", 5)

            class FakeClient:
                host = "fake"
                port = 0
                def fetch_updates(self, last_seen, ops=None, segment_hashes=None):
                    vv = replication_pb2.VersionVector(items=last_seen)
                    req = replication_pb2.FetchRequest(vector=vv, ops=ops or [], segment_hashes=segment_hashes or {})
                    return service_b.FetchUpdates(req, None)

                def close(self):
                    pass

            node_a.peer_clients = [FakeClient()]
            node_a.anti_entropy_interval = 0.1
            node_a._start_anti_entropy_thread()

            time.sleep(0.3)
            node_a._anti_entropy_stop.set()
            node_a._anti_entropy_thread.join()

            self.assertEqual(node_a.db.get("k"), "v")

            node_a.db.close()
            node_b.db.close()


class GetMultipleVersionsTest(unittest.TestCase):
    def test_get_returns_all_versions(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            node = NodeServer(db_path=tmpdir, node_id="A", peers=[])
            service = ReplicaService(node)

            vc_a = VectorClock({"A": 1})
            vc_b = VectorClock({"B": 1})
            node.db.put("k", "va", vector_clock=vc_a)
            node.db.put("k", "vb", vector_clock=vc_b)

            resp = service.Get(replication_pb2.KeyRequest(key="k", timestamp=0, node_id="test"), None)
            values = sorted(v.value for v in resp.values)
            self.assertEqual(values, ["va", "vb"])

            node.db.close()


class NodeInfoRPCTest(unittest.TestCase):
    def test_get_node_info_rpc(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            node = NodeServer(db_path=tmpdir, port=9100, node_id="A", peers=[])
            node.server.start()
            try:
                channel = grpc.insecure_channel(f"{node.host}:{node.port}")
                stub = replication_pb2_grpc.ReplicaStub(channel)
                req = replication_pb2.NodeInfoRequest(node_id="A")
                resp = stub.GetNodeInfo(req)
                self.assertEqual(resp.node_id, "A")
                self.assertTrue(resp.uptime >= 0)
                self.assertGreaterEqual(resp.replication_log_size, 0)
                self.assertGreaterEqual(resp.hints_count, 0)
                channel.close()
            finally:
                node.server.stop(0).wait()
                node.db.close()


class ReplicationStatusRPCTest(unittest.TestCase):
    def test_get_replication_status_rpc(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            node = NodeServer(db_path=tmpdir, port=9100, node_id="A", peers=[])
            node.server.start()
            try:
                channel = grpc.insecure_channel(f"{node.host}:{node.port}")
                stub = replication_pb2_grpc.ReplicaStub(channel)
                req = replication_pb2.NodeInfoRequest(node_id="A")
                resp = stub.GetReplicationStatus(req)
                self.assertEqual(dict(resp.last_seen), {})
                self.assertEqual(dict(resp.hints), {})
                channel.close()
            finally:
                node.server.stop(0).wait()
                node.db.close()


class StorageRPCTest(unittest.TestCase):
    def test_get_wal_entries_rpc(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            node = NodeServer(db_path=tmpdir, port=9101, node_id="A", peers=[])
            node.server.start()
            try:
                node.db.put("k1", "v1")
                node.db.put("k2", "v2")

                channel = grpc.insecure_channel(f"{node.host}:{node.port}")
                stub = replication_pb2_grpc.ReplicaStub(channel)
                req = replication_pb2.NodeInfoRequest(node_id="A")
                resp = stub.GetWalEntries(req)
                channel.close()

                self.assertEqual(len(resp.entries), 2)
                keys = sorted(entry.key for entry in resp.entries)
                self.assertEqual(keys, ["k1", "k2"])
            finally:
                node.server.stop(0).wait()
                node.db.close()

    def test_get_memtable_entries_rpc(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            node = NodeServer(db_path=tmpdir, port=9102, node_id="A", peers=[])
            node.server.start()
            try:
                node.db.put("k1", "v1")
                node.db.put("k2", "v2")

                channel = grpc.insecure_channel(f"{node.host}:{node.port}")
                stub = replication_pb2_grpc.ReplicaStub(channel)
                req = replication_pb2.NodeInfoRequest(node_id="A")
                resp = stub.GetMemtableEntries(req)
                channel.close()

                self.assertEqual(len(resp.entries), 2)
                keys = sorted(entry.key for entry in resp.entries)
                self.assertEqual(keys, ["k1", "k2"])
            finally:
                node.server.stop(0).wait()
                node.db.close()

    def test_get_sstables_rpc(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            node = NodeServer(db_path=tmpdir, port=9103, node_id="A", peers=[])
            node.server.start()
            # ensure the server is fully bound before issuing RPCs
            time.sleep(0.1)
            try:
                node.db.put("k1", "v1")
                node.db.put("k2", "v2")
                node.db._flush_memtable_to_sstable()

                channel = grpc.insecure_channel(f"{node.host}:{node.port}")
                stub = replication_pb2_grpc.ReplicaStub(channel)
                req = replication_pb2.NodeInfoRequest(node_id="A")
                resp = stub.GetSSTables(req)
                channel.close()

                self.assertTrue(len(resp.tables) >= 1)
                self.assertEqual(resp.tables[0].item_count, 2)
            finally:
                node.server.stop(0).wait()
                node.db.close()


if __name__ == "__main__":
    unittest.main()
