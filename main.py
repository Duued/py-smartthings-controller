import asyncio
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

SMARTTHINGS_API_KEY = os.getenv("SMARTTHINGS_API_KEY")