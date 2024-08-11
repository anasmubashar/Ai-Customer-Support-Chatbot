import os
from dotenv import load_dotenv

load_dotenv('.env.local')

GOOGLE_API_KEY = os.environ["NEXT_PUBLIC_GEMINI_KEY"]
print(GOOGLE_API_KEY)
KNOWLEDGE_BASE_PATH = r"api/data_structure_q_&_a.txt"