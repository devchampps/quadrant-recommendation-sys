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