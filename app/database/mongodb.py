from pymongo import MongoClient
from pymongo.errors import PyMongoError

from app.config.settings import settings

# Create one client for the whole application and reuse it.
client = MongoClient(settings.MONGO_URI, serverSelectionTimeoutMS=5000)
db = client[settings.MONGO_DATABASE]


def get_database():
    """Return the configured database instance."""
    return db


def get_collection(collection_name: str):
    """Return a named collection, creating it if it does not exist yet."""
    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name)

    collection = db[collection_name]
    if collection_name == "products":
        try:
            index_info = collection.index_information()
            for index_name, index_details in index_info.items():
                key = index_details.get("key") if isinstance(index_details, dict) else None
                if index_name == "sku_1" or key == [("sku", 1)]:
                    collection.drop_index(index_name)
        except Exception:
            pass

    return collection


def ping_database():
    """Check whether MongoDB responds to a ping request."""
    try:
        client.admin.command("ping")
        return {"status": "ok", "database": settings.MONGO_DATABASE}
    except PyMongoError as exc:
        raise RuntimeError(f"MongoDB connection failed: {exc}") from exc
