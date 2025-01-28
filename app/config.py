# app/config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# AWS Credentials
AWS_ACCESS_KEY = os.getenv("MY_AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("MY_AWS_SECRET_KEY")
REGION_NAME = os.getenv("AWS_REGION")

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_DB = os.getenv("REDIS_DB")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_USERNAME = os.getenv("REDIS_USERNAME")