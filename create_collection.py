from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.models import PointStruct


DB_URL = "http://localhost"
DB_PORT = "6333"    
SERVER_URL = DB_URL + ":" + DB_PORT
COLECTION_NAME = "Jobs"


client = QdrantClient(url=SERVER_URL)

operation_info = client.create_collection(
    collection_name=COLECTION_NAME,
    vectors_config=VectorParams(size=1536, distance=Distance.DOT),
)


print(operation_info)