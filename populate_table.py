import feedparser
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
RSS_XML_URL = "https://rss.mustakbil.com/jobs-rss"

"""RSS_XML_URL = "https://rss.mustakbil.com/jobs/xml/pakistan"
"""

def read_rss_feed(url):
    """
    Reads and parses an RSS feed from a given URL.

    Args:
        url (str): The URL of the RSS feed.

    Returns:
        dict: A dictionary containing the parsed feed data, 
              or None if an error occurs.
    """
    try:
        feed = feedparser.parse(url)
        if feed.bozo == 1:
            print(f"Error parsing feed: {feed.bozo_exception}")
            return None
        return feed
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def format_feeddata(feed_data):
    """
        Format the feed data per requirements. For our case, we just need to concatenate  job title and description, and return list. 
    """
    if feed_data:
        count = 0
        concatString =""
        jobId=""
        jobTitle = ""
        jobDescription = ""
        jobUrl=""
        jobpostedOn=""
        jobType=""
        salary=""
        jobCategory=""
        company=""
        city=""
        country=""
        
        jobsList = []

        for entry in feed_data.entries:
            jobObject={}
            jobTitle = entry.title
            jobDescription = entry.description

            ##jobObject["jobId"] = entry.id
            jobObject["jobTitle"] = entry.title
            jobObject["jobDescription"] = entry.description
            jobObject["jobUrl"] = entry.link

            jobObject["jobCategory"] = entry.category
            jobObject["company"] = entry.company
            jobObject["city"] = entry.city
            jobObject["country"] = entry.country
            count = count + 1
            jobsList.append(jobObject)
            
        print("Total Jobs count in feed :" + str(count) )
        print(jobsList[11])
        return jobsList    
    else:
        print("Failed to read or parse the RSS feed.")
        return ""
    
def create_embeddings_populate_table(data):
    OpenAI_client = OpenAI(api_key=OPENAI_API_KEY)
    Quadrant_client = QdrantClient(url=SERVER_URL)
    data_id = 1
    embedding_input =""
    
    for entry in data:
        print(type(entry))
        #exit -1
        embedding_input = str(entry["jobTitle"]) + " " + str(entry["jobDescription"])
        data_embedding = OpenAI_client.embeddings.create(
        input=str(embedding_input),
        model="text-embedding-3-small"
        )


        '''Upsert into table '''   
        
        upsert_status = Quadrant_client.upsert(
        collection_name="Jobs",
        wait=True,
        points=[
            PointStruct(id=data_id, vector=data_embedding.data[0].embedding, payload=entry),
            ],
        )
        data_id = data_id + 1

    
        

if __name__ == '__main__':
    feed_data = read_rss_feed(RSS_XML_URL)
    data = format_feeddata(feed_data)
    
    create_embeddings_populate_table(data)
