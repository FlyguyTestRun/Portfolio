"""Azure Cosmos DB client for durable checkpoint storage. In local mode, uses an
in-memory dict. In hybrid/cloud mode, connects to Azure Cosmos DB NoSQL API."""

from __future__ import annotations

from falcon_grounds.config import COSMOS_DB_NAME, COSMOS_KEY, COSMOS_URL, RUNTIME_MODE, RuntimeMode


class CosmosClient:
    """Checkpoint store backed by Cosmos DB in cloud or in-memory in local mode."""

    def __init__(self) -> None:
        self._store: dict[str, dict] = {}
        self._container = None
        if RUNTIME_MODE == RuntimeMode.LOCAL:
            return
        if not (COSMOS_URL and COSMOS_KEY):
            return
        try:
            from azure.cosmos import CosmosClient as _CosmosClient
            client = _CosmosClient(COSMOS_URL, credential=COSMOS_KEY)
            db = client.get_database_client(COSMOS_DB_NAME)
            self._container = db.get_container_client("checkpoints")
        except Exception:
            pass

    def save_checkpoint(self, run_id: str, state: dict) -> None:
        """Persist graph state keyed by run_id."""
        if self._container is not None:
            try:
                self._container.upsert_item({"id": run_id, **state})
                return
            except Exception:
                pass
        self._store[run_id] = state

    def load_checkpoint(self, run_id: str) -> dict | None:
        """Retrieve graph state by run_id."""
        if self._container is not None:
            try:
                return self._container.read_item(item=run_id, partition_key=run_id)
            except Exception:
                pass
        return self._store.get(run_id)


_cosmos_instance: CosmosClient | None = None


def get_cosmos_client() -> CosmosClient:
    global _cosmos_instance
    if _cosmos_instance is None:
        _cosmos_instance = CosmosClient()
    return _cosmos_instance
