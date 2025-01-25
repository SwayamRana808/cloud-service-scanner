from fastapi import APIRouter, Request  # Add Request here
from app.services.aws_services import get_ec2_instances
from app.services.assessment_engine import assess_security_group

router = APIRouter()

@router.get("/scan/ec2")
async def scan_ec2():
    """
    API endpoint to scan EC2 instances.
    """
    instances = get_ec2_instances()
    issues = []
    for instance in instances:
        security_groups = instance['Instances'][0].get('SecurityGroups', [])
        for sg in security_groups:
            issue = assess_security_group(sg)
            if issue:
                issues.append(issue)
    return {"issues": issues}

@router.post("/scan/ec2")
async def scan_ec2(request: Request):
    # Get the event data from the body
    event_data = await request.json()
    
    # Parse the EC2 instance information from the event
    instance_id = event_data.get("detail", {}).get("instance-id")
    
    if not instance_id:
        return {"error": "Instance ID not found in event data"}
    
    # Fetch the EC2 instance details using Boto3
    instances = get_ec2_instances(instance_id=instance_id)
    
    # Check the security groups for the EC2 instance
    issues = []
    for instance in instances:
        security_groups = instance['Instances'][0].get('SecurityGroups', [])
        for sg in security_groups:
            issue = assess_security_group(sg)
            if issue:
                issues.append(issue)
    
    # Return any security issues found
    return {"instance_id": instance_id, "issues": issues}
