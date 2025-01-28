import boto3
from app.config import AWS_ACCESS_KEY, AWS_SECRET_KEY 
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, BotoCoreError

def get_security_groups():
    """
    Retrieve all security groups across multiple regions.
    Handles potential AWS credential and connection errors.
    """
    try:
        regions = ['us-east-1', 'ap-south-1', 'ap-northeast-3']  # Extend as needed
        all_security_groups = {}

        for region in regions:
            ec2_client = boto3.client(
                'ec2',
                aws_access_key_id=AWS_ACCESS_KEY,
                aws_secret_access_key=AWS_SECRET_KEY,
                region_name=region
            )
            response = ec2_client.describe_security_groups()
            security_groups = response.get('SecurityGroups', [])
            all_security_groups[region] = security_groups

        return all_security_groups

    except NoCredentialsError:
        return {"error": "AWS credentials not found."}

    except PartialCredentialsError:
        return {"error": "Incomplete AWS credentials."}

    except BotoCoreError as e:
        return {"error": f"Boto3 error: {str(e)}"}

    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}
