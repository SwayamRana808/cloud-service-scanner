import boto3
from app.config import AWS_ACCESS_KEY, AWS_SECRET_KEY, REGION_NAME
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, BotoCoreError


def get_rds_instances():
    """
    Retrieve all RDS instances across all available regions.
    Handles potential AWS credential and connection errors.
    """
    try:
        # Get all available regions for the RDS service
        regions = ['us-east-1', 'ap-south-1']
        all_instances = {}

        for region in regions:
            # Create an RDS client for the current region
            rds_region_client = boto3.client(
                'rds',
                aws_access_key_id=AWS_ACCESS_KEY,
                aws_secret_access_key=AWS_SECRET_KEY,
                region_name=region,
            )

            # Describe RDS instances in the current region
            response = rds_region_client.describe_db_instances()

            # Extract instances from the response
            instances = response.get('DBInstances', [])
            if instances:
                all_instances[region] = instances

        return all_instances

    except NoCredentialsError:
        return {"error": "AWS credentials not found."}

    except PartialCredentialsError:
        return {"error": "Incomplete AWS credentials."}

    except BotoCoreError as e:
        return {"error": f"Boto3 error: {str(e)}"}

    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}
