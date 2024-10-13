from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()


mongodb_uri = os.getenv("DATABASE_URL")

client = MongoClient(mongodb_uri, server_api=ServerApi('1'))

db = client.fastapi_assignment
items_collection = db['items']
clockins_collection = db['clockins']