from api.main import app
from database.replication import NodeCluster
from .service_runner import start_frontend
from .data_generators import generate_hash_items


def main() -> None:
    app.router.on_startup.clear()
    ranges = [("a", "m"), ("m", "z")]
    cluster = NodeCluster(
        base_path="/tmp/registry_cluster",
        num_nodes=2,
        key_ranges=ranges,
        start_router=True,
        use_registry=True,
    )

    print("Partitions:")
    for pid, owner in sorted(cluster.get_partition_map().items()):
        rng = cluster.partitions[pid][0]
        print(f"  P{pid} {rng} -> {owner}")

    for key, value in generate_hash_items(50):
        cluster.router_client.put(key, value)
        pid = cluster.get_partition_id(key)
        owner = cluster.get_partition_map().get(pid)
        rng = cluster.partitions[pid][0]
        print(
            f"Router stored {key} -> {value} in partition {pid} {rng} on {owner}"
        )
    app.state.cluster = cluster
    front_proc = start_frontend()
    print("API running at http://localhost:8000")
    try:
        import uvicorn
        uvicorn.run("api.main:app", port=8000)
    finally:
        front_proc.terminate()
        cluster.shutdown()


if __name__ == "__main__":
    main()
