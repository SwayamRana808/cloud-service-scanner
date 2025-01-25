from dotenv import load_dotenv
import os

load_dotenv()

print("AWS Access Key:", os.getenv("AWS_ACCESS_KEY"))
print("AWS Region:", os.getenv("AWS_REGION"))
