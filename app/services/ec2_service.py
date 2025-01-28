import boto3
from app.config import AWS_ACCESS_KEY, AWS_SECRET_KEY, REGION_NAME
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, BotoCoreError

def get_ec2_instances():
    """
    Retrieve all EC2 instances across all available regions.
    Handles potential AWS credential and connection errors.
    """
    try:
        
        # Get all available regions for EC2 service
        regions =  ['us-east-1','ap-south-1','ap-northeast-3']
        all_instances = {}
        print(regions)
        # Iterate through each region and get instances
        for region in regions :
             
            
            # Create EC2 client for the current region
            ec2_region_client = boto3.client('ec2', 
                                             aws_access_key_id=AWS_ACCESS_KEY,
                                             aws_secret_access_key=AWS_SECRET_KEY,
                                             region_name=region)
            
            # Describe instances for the current region
            response = ec2_region_client.describe_instances()
            
            # Extract instances from the response
            instances = response.get('Reservations', [])
            
            if instances:
                all_instances[region] = instances

        return all_instances

    except NoCredentialsError:
        # Handle the case where AWS credentials are missing
        return {"error": "AWS credentials not found."}

    except PartialCredentialsError:
        # Handle the case where AWS credentials are incomplete
        return {"error": "Incomplete AWS credentials."}

    except BotoCoreError as e:
        # Handle other boto3-related errors (e.g., connection issues)
        return {"error": f"Boto3 error: {str(e)}"}

    except Exception as e:
        # Catch all other exceptions and log them
        return {"error": f"An unexpected error occurred: {str(e)}"}
 