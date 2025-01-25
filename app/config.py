# app/config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# AWS Credentials
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
REGION_NAME = os.getenv("AWS_REGION")

