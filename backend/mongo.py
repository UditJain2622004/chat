# MongoDB connection setup for backend

from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
print("MongoDB Connection Successful")
db = client['chat_db']  # Use your desired database name

"""
mongo.py: Handles MongoDB connection only
"""
