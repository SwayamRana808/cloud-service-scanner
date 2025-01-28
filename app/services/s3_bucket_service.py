import boto3
from app.config import AWS_ACCESS_KEY, AWS_SECRET_KEY 
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, BotoCoreError


def get_s3_buckets():
    """
    Retrieve all S3 buckets in the account.
    Handles potential AWS credential and connection errors.
    """
    try:
        # Create an S3 client
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
        )

        # List all S3 buckets
        response = s3_client.list_buckets()
        # Extract buckets from the response
        buckets = response.get('Buckets', [])

         
        return buckets

    except NoCredentialsError:
        return {"error": "AWS credentials not found."}

    except PartialCredentialsError:
        return {"error": "Incomplete AWS credentials."}

    except BotoCoreError as e:
        return {"error": f"Boto3 error: {str(e)}"}

    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}
