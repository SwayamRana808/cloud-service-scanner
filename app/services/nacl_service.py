import boto3
from app.config import AWS_ACCESS_KEY, AWS_SECRET_KEY
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, BotoCoreError


def get_network_acls():
    """
    Fetch all Network ACLs (NACLs) across all specified regions.
    Handles potential AWS credential and connection errors.
    """
    regions = ['us-east-1', 'ap-south-1', 'ap-northeast-3']
    nacls_by_region = {}

    for region in regions:
        try:
            ec2_client = boto3.client(
                'ec2',
                aws_access_key_id=AWS_ACCESS_KEY,
                aws_secret_access_key=AWS_SECRET_KEY,
                region_name=region,
            )
            response = ec2_client.describe_network_acls()
            nacls = response.get("NetworkAcls", [])
            nacls_by_region[region] = nacls

        except NoCredentialsError:
            nacls_by_region[region] = {"error": "AWS credentials not found."}

        except PartialCredentialsError:
            nacls_by_region[region] = {"error": "Incomplete AWS credentials."}

        except BotoCoreError as e:
            nacls_by_region[region] = {"error": f"Boto3 error: {str(e)}"}

        except Exception as e:
            nacls_by_region[region] = {"error": f"Unexpected error: {str(e)}"}

    return nacls_by_region
