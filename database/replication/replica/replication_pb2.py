# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: replication.proto
# Protobuf Python Version: 6.31.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    6,
    31,
    0,
    '',
    'replication.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11replication.proto\x12\x0breplication\"\xb0\x01\n\nKeyRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x11\n\ttimestamp\x18\x02 \x01(\x03\x12\x0f\n\x07node_id\x18\x03 \x01(\t\x12\r\n\x05op_id\x18\x04 \x01(\t\x12*\n\x06vector\x18\x05 \x01(\x0b\x32\x1a.replication.VersionVector\x12\x12\n\nhinted_for\x18\x06 \x01(\t\x12\x13\n\x0bin_progress\x18\x07 \x03(\t\x12\r\n\x05tx_id\x18\x08 \x01(\t\"\xa8\x01\n\x08KeyValue\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\x12\x11\n\ttimestamp\x18\x03 \x01(\x03\x12\x0f\n\x07node_id\x18\x04 \x01(\t\x12\r\n\x05op_id\x18\x05 \x01(\t\x12*\n\x06vector\x18\x06 \x01(\x0b\x32\x1a.replication.VersionVector\x12\x12\n\nhinted_for\x18\x07 \x01(\t\x12\r\n\x05tx_id\x18\x08 \x01(\t\"/\n\x10IncrementRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x0e\n\x06\x61mount\x18\x02 \x01(\x03\"C\n\x0fTransferRequest\x12\x10\n\x08\x66rom_key\x18\x01 \x01(\t\x12\x0e\n\x06to_key\x18\x02 \x01(\t\x12\x0e\n\x06\x61mount\x18\x03 \x01(\x03\"^\n\x0eVersionedValue\x12\r\n\x05value\x18\x01 \x01(\t\x12\x11\n\ttimestamp\x18\x02 \x01(\x03\x12*\n\x06vector\x18\x03 \x01(\x0b\x32\x1a.replication.VersionVector\"<\n\rValueResponse\x12+\n\x06values\x18\x01 \x03(\x0b\x32\x1b.replication.VersionedValue\"G\n\x0cRangeRequest\x12\x15\n\rpartition_key\x18\x01 \x01(\t\x12\x10\n\x08start_ck\x18\x02 \x01(\t\x12\x0e\n\x06\x65nd_ck\x18\x03 \x01(\t\"q\n\tRangeItem\x12\x16\n\x0e\x63lustering_key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\x12\x11\n\ttimestamp\x18\x03 \x01(\x03\x12*\n\x06vector\x18\x04 \x01(\x0b\x32\x1a.replication.VersionVector\"6\n\rRangeResponse\x12%\n\x05items\x18\x01 \x03(\x0b\x32\x16.replication.RangeItem\"\x07\n\x05\x45mpty\"\x1c\n\tHeartbeat\x12\x0f\n\x07node_id\x18\x01 \x01(\t\"0\n\rTransactionId\x12\n\n\x02id\x18\x01 \x01(\t\x12\x13\n\x0bin_progress\x18\x02 \x03(\t\"#\n\x12TransactionControl\x12\r\n\x05tx_id\x18\x01 \x01(\t\"!\n\x0fTransactionList\x12\x0e\n\x06tx_ids\x18\x01 \x03(\t\"s\n\rVersionVector\x12\x34\n\x05items\x18\x01 \x03(\x0b\x32%.replication.VersionVector.ItemsEntry\x1a,\n\nItemsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x03:\x02\x38\x01\"q\n\x0cPartitionMap\x12\x33\n\x05items\x18\x01 \x03(\x0b\x32$.replication.PartitionMap.ItemsEntry\x1a,\n\nItemsEntry\x12\x0b\n\x03key\x18\x01 \x01(\x05\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\".\n\rHashRingEntry\x12\x0c\n\x04hash\x18\x01 \x01(\t\x12\x0f\n\x07node_id\x18\x02 \x01(\t\"5\n\x08HashRing\x12)\n\x05items\x18\x01 \x03(\x0b\x32\x1a.replication.HashRingEntry\"\x7f\n\rMerkleNodeMsg\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x0c\n\x04hash\x18\x02 \x01(\t\x12(\n\x04left\x18\x03 \x01(\x0b\x32\x1a.replication.MerkleNodeMsg\x12)\n\x05right\x18\x04 \x01(\x0b\x32\x1a.replication.MerkleNodeMsg\"H\n\x0bSegmentTree\x12\x0f\n\x07segment\x18\x01 \x01(\t\x12(\n\x04root\x18\x02 \x01(\x0b\x32\x1a.replication.MerkleNodeMsg\"\x96\x01\n\tOperation\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\x12\x11\n\ttimestamp\x18\x03 \x01(\x03\x12\x0f\n\x07node_id\x18\x04 \x01(\t\x12\r\n\x05op_id\x18\x05 \x01(\t\x12\x0e\n\x06\x64\x65lete\x18\x06 \x01(\x08\x12*\n\x06vector\x18\x07 \x01(\x0b\x32\x1a.replication.VersionVector\"\x84\x02\n\x0c\x46\x65tchRequest\x12*\n\x06vector\x18\x01 \x01(\x0b\x32\x1a.replication.VersionVector\x12#\n\x03ops\x18\x02 \x03(\x0b\x32\x16.replication.Operation\x12\x44\n\x0esegment_hashes\x18\x03 \x03(\x0b\x32,.replication.FetchRequest.SegmentHashesEntry\x12\'\n\x05trees\x18\x04 \x03(\x0b\x32\x18.replication.SegmentTree\x1a\x34\n\x12SegmentHashesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\xb1\x01\n\rFetchResponse\x12#\n\x03ops\x18\x01 \x03(\x0b\x32\x16.replication.Operation\x12\x45\n\x0esegment_hashes\x18\x02 \x03(\x0b\x32-.replication.FetchResponse.SegmentHashesEntry\x1a\x34\n\x12SegmentHashesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"*\n\nIndexQuery\x12\r\n\x05\x66ield\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"\x17\n\x07KeyList\x12\x0c\n\x04keys\x18\x01 \x03(\t\"\xa0\x01\n\x0fNodeInfoRequest\x12\x0f\n\x07node_id\x18\x01 \x01(\t\x12\x0e\n\x06status\x18\x02 \x01(\t\x12\x0b\n\x03\x63pu\x18\x03 \x01(\x01\x12\x0e\n\x06memory\x18\x04 \x01(\x01\x12\x0c\n\x04\x64isk\x18\x05 \x01(\x01\x12\x0e\n\x06uptime\x18\x06 \x01(\x03\x12\x1c\n\x14replication_log_size\x18\x07 \x01(\x05\x12\x13\n\x0bhints_count\x18\x08 \x01(\x05\"\xa1\x01\n\x10NodeInfoResponse\x12\x0f\n\x07node_id\x18\x01 \x01(\t\x12\x0e\n\x06status\x18\x02 \x01(\t\x12\x0b\n\x03\x63pu\x18\x03 \x01(\x01\x12\x0e\n\x06memory\x18\x04 \x01(\x01\x12\x0c\n\x04\x64isk\x18\x05 \x01(\x01\x12\x0e\n\x06uptime\x18\x06 \x01(\x03\x12\x1c\n\x14replication_log_size\x18\x07 \x01(\x05\x12\x13\n\x0bhints_count\x18\x08 \x01(\x05\"\x85\x02\n\x19ReplicationStatusResponse\x12G\n\tlast_seen\x18\x01 \x03(\x0b\x32\x34.replication.ReplicationStatusResponse.LastSeenEntry\x12@\n\x05hints\x18\x02 \x03(\x0b\x32\x31.replication.ReplicationStatusResponse.HintsEntry\x1a/\n\rLastSeenEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x03:\x02\x38\x01\x1a,\n\nHintsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\"`\n\x08WalEntry\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\x0b\n\x03key\x18\x02 \x01(\t\x12\r\n\x05value\x18\x03 \x01(\t\x12*\n\x06vector\x18\x04 \x01(\x0b\x32\x1a.replication.VersionVector\"<\n\x12WalEntriesResponse\x12&\n\x07\x65ntries\x18\x01 \x03(\x0b\x32\x15.replication.WalEntry\"V\n\x0cStorageEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\x12*\n\x06vector\x18\x03 \x01(\x0b\x32\x1a.replication.VersionVector\"D\n\x16StorageEntriesResponse\x12*\n\x07\x65ntries\x18\x01 \x03(\x0b\x32\x19.replication.StorageEntry\"n\n\x0bSSTableInfo\x12\n\n\x02id\x18\x01 \x01(\t\x12\r\n\x05level\x18\x02 \x01(\x05\x12\x0c\n\x04size\x18\x03 \x01(\x03\x12\x12\n\nitem_count\x18\x04 \x01(\x05\x12\x11\n\tstart_key\x18\x05 \x01(\t\x12\x0f\n\x07\x65nd_key\x18\x06 \x01(\t\"?\n\x13SSTableInfoResponse\x12(\n\x06tables\x18\x01 \x03(\x0b\x32\x18.replication.SSTableInfo\"<\n\x15SSTableContentRequest\x12\x0f\n\x07node_id\x18\x01 \x01(\t\x12\x12\n\nsstable_id\x18\x02 \x01(\t2\xd9\x0b\n\x07Replica\x12\x30\n\x03Put\x12\x15.replication.KeyValue\x1a\x12.replication.Empty\x12\x35\n\x06\x44\x65lete\x12\x17.replication.KeyRequest\x1a\x12.replication.Empty\x12:\n\x03Get\x12\x17.replication.KeyRequest\x1a\x1a.replication.ValueResponse\x12\x43\n\x0cGetForUpdate\x12\x17.replication.KeyRequest\x1a\x1a.replication.ValueResponse\x12>\n\tIncrement\x12\x1d.replication.IncrementRequest\x1a\x12.replication.Empty\x12<\n\x08Transfer\x12\x1c.replication.TransferRequest\x1a\x12.replication.Empty\x12\x42\n\x10\x42\x65ginTransaction\x12\x12.replication.Empty\x1a\x1a.replication.TransactionId\x12H\n\x11\x43ommitTransaction\x12\x1f.replication.TransactionControl\x1a\x12.replication.Empty\x12G\n\x10\x41\x62ortTransaction\x12\x1f.replication.TransactionControl\x1a\x12.replication.Empty\x12\x44\n\x10ListTransactions\x12\x12.replication.Empty\x1a\x1c.replication.TransactionList\x12\x42\n\tScanRange\x12\x19.replication.RangeRequest\x1a\x1a.replication.RangeResponse\x12\x45\n\x0c\x46\x65tchUpdates\x12\x19.replication.FetchRequest\x1a\x1a.replication.FetchResponse\x12\x43\n\x12UpdatePartitionMap\x12\x19.replication.PartitionMap\x1a\x12.replication.Empty\x12;\n\x0eUpdateHashRing\x12\x15.replication.HashRing\x1a\x12.replication.Empty\x12<\n\x0bListByIndex\x12\x17.replication.IndexQuery\x1a\x14.replication.KeyList\x12J\n\x0bGetNodeInfo\x12\x1c.replication.NodeInfoRequest\x1a\x1d.replication.NodeInfoResponse\x12\\\n\x14GetReplicationStatus\x12\x1c.replication.NodeInfoRequest\x1a&.replication.ReplicationStatusResponse\x12N\n\rGetWalEntries\x12\x1c.replication.NodeInfoRequest\x1a\x1f.replication.WalEntriesResponse\x12W\n\x12GetMemtableEntries\x12\x1c.replication.NodeInfoRequest\x1a#.replication.StorageEntriesResponse\x12M\n\x0bGetSSTables\x12\x1c.replication.NodeInfoRequest\x1a .replication.SSTableInfoResponse\x12\\\n\x11GetSSTableContent\x12\".replication.SSTableContentRequest\x1a#.replication.StorageEntriesResponse2F\n\x10HeartbeatService\x12\x32\n\x04Ping\x12\x16.replication.Heartbeat\x1a\x12.replication.Emptyb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'replication_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_VERSIONVECTOR_ITEMSENTRY']._loaded_options = None
  _globals['_VERSIONVECTOR_ITEMSENTRY']._serialized_options = b'8\001'
  _globals['_PARTITIONMAP_ITEMSENTRY']._loaded_options = None
  _globals['_PARTITIONMAP_ITEMSENTRY']._serialized_options = b'8\001'
  _globals['_FETCHREQUEST_SEGMENTHASHESENTRY']._loaded_options = None
  _globals['_FETCHREQUEST_SEGMENTHASHESENTRY']._serialized_options = b'8\001'
  _globals['_FETCHRESPONSE_SEGMENTHASHESENTRY']._loaded_options = None
  _globals['_FETCHRESPONSE_SEGMENTHASHESENTRY']._serialized_options = b'8\001'
  _globals['_REPLICATIONSTATUSRESPONSE_LASTSEENENTRY']._loaded_options = None
  _globals['_REPLICATIONSTATUSRESPONSE_LASTSEENENTRY']._serialized_options = b'8\001'
  _globals['_REPLICATIONSTATUSRESPONSE_HINTSENTRY']._loaded_options = None
  _globals['_REPLICATIONSTATUSRESPONSE_HINTSENTRY']._serialized_options = b'8\001'
  _globals['_KEYREQUEST']._serialized_start=35
  _globals['_KEYREQUEST']._serialized_end=211
  _globals['_KEYVALUE']._serialized_start=214
  _globals['_KEYVALUE']._serialized_end=382
  _globals['_INCREMENTREQUEST']._serialized_start=384
  _globals['_INCREMENTREQUEST']._serialized_end=431
  _globals['_TRANSFERREQUEST']._serialized_start=433
  _globals['_TRANSFERREQUEST']._serialized_end=500
  _globals['_VERSIONEDVALUE']._serialized_start=502
  _globals['_VERSIONEDVALUE']._serialized_end=596
  _globals['_VALUERESPONSE']._serialized_start=598
  _globals['_VALUERESPONSE']._serialized_end=658
  _globals['_RANGEREQUEST']._serialized_start=660
  _globals['_RANGEREQUEST']._serialized_end=731
  _globals['_RANGEITEM']._serialized_start=733
  _globals['_RANGEITEM']._serialized_end=846
  _globals['_RANGERESPONSE']._serialized_start=848
  _globals['_RANGERESPONSE']._serialized_end=902
  _globals['_EMPTY']._serialized_start=904
  _globals['_EMPTY']._serialized_end=911
  _globals['_HEARTBEAT']._serialized_start=913
  _globals['_HEARTBEAT']._serialized_end=941
  _globals['_TRANSACTIONID']._serialized_start=943
  _globals['_TRANSACTIONID']._serialized_end=991
  _globals['_TRANSACTIONCONTROL']._serialized_start=993
  _globals['_TRANSACTIONCONTROL']._serialized_end=1028
  _globals['_TRANSACTIONLIST']._serialized_start=1030
  _globals['_TRANSACTIONLIST']._serialized_end=1063
  _globals['_VERSIONVECTOR']._serialized_start=1065
  _globals['_VERSIONVECTOR']._serialized_end=1180
  _globals['_VERSIONVECTOR_ITEMSENTRY']._serialized_start=1136
  _globals['_VERSIONVECTOR_ITEMSENTRY']._serialized_end=1180
  _globals['_PARTITIONMAP']._serialized_start=1182
  _globals['_PARTITIONMAP']._serialized_end=1295
  _globals['_PARTITIONMAP_ITEMSENTRY']._serialized_start=1251
  _globals['_PARTITIONMAP_ITEMSENTRY']._serialized_end=1295
  _globals['_HASHRINGENTRY']._serialized_start=1297
  _globals['_HASHRINGENTRY']._serialized_end=1343
  _globals['_HASHRING']._serialized_start=1345
  _globals['_HASHRING']._serialized_end=1398
  _globals['_MERKLENODEMSG']._serialized_start=1400
  _globals['_MERKLENODEMSG']._serialized_end=1527
  _globals['_SEGMENTTREE']._serialized_start=1529
  _globals['_SEGMENTTREE']._serialized_end=1601
  _globals['_OPERATION']._serialized_start=1604
  _globals['_OPERATION']._serialized_end=1754
  _globals['_FETCHREQUEST']._serialized_start=1757
  _globals['_FETCHREQUEST']._serialized_end=2017
  _globals['_FETCHREQUEST_SEGMENTHASHESENTRY']._serialized_start=1965
  _globals['_FETCHREQUEST_SEGMENTHASHESENTRY']._serialized_end=2017
  _globals['_FETCHRESPONSE']._serialized_start=2020
  _globals['_FETCHRESPONSE']._serialized_end=2197
  _globals['_FETCHRESPONSE_SEGMENTHASHESENTRY']._serialized_start=1965
  _globals['_FETCHRESPONSE_SEGMENTHASHESENTRY']._serialized_end=2017
  _globals['_INDEXQUERY']._serialized_start=2199
  _globals['_INDEXQUERY']._serialized_end=2241
  _globals['_KEYLIST']._serialized_start=2243
  _globals['_KEYLIST']._serialized_end=2266
  _globals['_NODEINFOREQUEST']._serialized_start=2269
  _globals['_NODEINFOREQUEST']._serialized_end=2429
  _globals['_NODEINFORESPONSE']._serialized_start=2432
  _globals['_NODEINFORESPONSE']._serialized_end=2593
  _globals['_REPLICATIONSTATUSRESPONSE']._serialized_start=2596
  _globals['_REPLICATIONSTATUSRESPONSE']._serialized_end=2857
  _globals['_REPLICATIONSTATUSRESPONSE_LASTSEENENTRY']._serialized_start=2764
  _globals['_REPLICATIONSTATUSRESPONSE_LASTSEENENTRY']._serialized_end=2811
  _globals['_REPLICATIONSTATUSRESPONSE_HINTSENTRY']._serialized_start=2813
  _globals['_REPLICATIONSTATUSRESPONSE_HINTSENTRY']._serialized_end=2857
  _globals['_WALENTRY']._serialized_start=2859
  _globals['_WALENTRY']._serialized_end=2955
  _globals['_WALENTRIESRESPONSE']._serialized_start=2957
  _globals['_WALENTRIESRESPONSE']._serialized_end=3017
  _globals['_STORAGEENTRY']._serialized_start=3019
  _globals['_STORAGEENTRY']._serialized_end=3105
  _globals['_STORAGEENTRIESRESPONSE']._serialized_start=3107
  _globals['_STORAGEENTRIESRESPONSE']._serialized_end=3175
  _globals['_SSTABLEINFO']._serialized_start=3177
  _globals['_SSTABLEINFO']._serialized_end=3287
  _globals['_SSTABLEINFORESPONSE']._serialized_start=3289
  _globals['_SSTABLEINFORESPONSE']._serialized_end=3352
  _globals['_SSTABLECONTENTREQUEST']._serialized_start=3354
  _globals['_SSTABLECONTENTREQUEST']._serialized_end=3414
  _globals['_REPLICA']._serialized_start=3417
  _globals['_REPLICA']._serialized_end=4914
  _globals['_HEARTBEATSERVICE']._serialized_start=4916
  _globals['_HEARTBEATSERVICE']._serialized_end=4986
# @@protoc_insertion_point(module_scope)
