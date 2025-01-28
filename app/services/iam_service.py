import boto3
from app.config import AWS_ACCESS_KEY, AWS_SECRET_KEY, REGION_NAME
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, BotoCoreError


def get_iam_users():
    """
    Retrieve all IAM users in the account.
    Handles potential AWS credential and connection errors.
    """
    try:
        # Create an IAM client
        iam_client = boto3.client(
            'iam',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
        )

        # Paginate through all IAM users
        paginator = iam_client.get_paginator('list_users')
        response_iterator = paginator.paginate()

        all_users = []
        for page in response_iterator:
            all_users.extend(page.get('Users', []))

        return all_users

    except NoCredentialsError:
        return {"error": "AWS credentials not found."}

    except PartialCredentialsError:
        return {"error": "Incomplete AWS credentials."}

    except BotoCoreError as e:
        return {"error": f"Boto3 error: {str(e)}"}

    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}
