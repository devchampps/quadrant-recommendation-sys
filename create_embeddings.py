from openai import OpenAI
import os

from ssm import get_secret

secret_name = "devchampps/openai/OPENAI_API_KEY"
region_name = "ap-southeast-2"
OPENAI_API_KEY=get_secret(secret_name, region_name)

client = OpenAI(api_key=OPENAI_API_KEY)

response = client.embeddings.create(
    input="Your text string goes here",
    model="text-embedding-3-small"
)


print(response.data[0].embedding)


