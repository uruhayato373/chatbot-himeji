import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_ENVIRONMENT_REGION = os.environ.get("PINECONE_ENVIRONMENT_REGION")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")