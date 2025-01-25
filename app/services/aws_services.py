import boto3
from app.config import AWS_ACCESS_KEY, AWS_SECRET_KEY, REGION_NAME
def get_ec2_instances():
    """
    Retrieve all EC2 instances in the default region.
    """
    ec2_client = boto3.client('ec2', 
                              aws_access_key_id=AWS_ACCESS_KEY,
                              aws_secret_access_key=AWS_SECRET_KEY,
                              region_name=REGION_NAME)
    response = ec2_client.describe_instances()
    instances = response.get('Reservations', [])
    return instances
