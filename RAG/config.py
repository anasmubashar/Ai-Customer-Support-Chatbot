import os
from dotenv import load_dotenv

load_dotenv('.env.local')

GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]

KNOWLEDGE_BASE_PATH = ""