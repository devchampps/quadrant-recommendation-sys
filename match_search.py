from openai import OpenAI
import os

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.models import PointStruct

from ssm import get_secret

secret_name = "devchampps/openai/OPENAI_API_KEY"
region_name = "ap-southeast-2"
OPENAI_API_KEY=get_secret(secret_name, region_name)
DB_URL = "http://localhost"
DB_PORT = "6333"
SERVER_URL = DB_URL + ":" + DB_PORT
COLECTION_NAME = "Jobs"

OpenAI_client = OpenAI(api_key=OPENAI_API_KEY)
Quadrant_client = QdrantClient(url=SERVER_URL)


searchString ="Software Developer"
searchString_embedding = OpenAI_client.embeddings.create(
        input=str(searchString),
        model="text-embedding-3-small"
        )

search_result = Quadrant_client.query_points(
    collection_name="Jobs",
    query=searchString_embedding.data[0].embedding,
    with_payload=True,
    limit=3
).points


print("type of Search result : " + str(type(search_result)))
for item in search_result:
    print("Similarity Match" + str(item.score) + "\n")
    print("JOb Title" + str(item.payload["jobTitle"]) + "\n")

