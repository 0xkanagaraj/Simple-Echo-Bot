import os
from dotenv import load_dotenv

#Load bot token from .env file / environment variables
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")