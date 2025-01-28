import boto3
from app.config import AWS_ACCESS_KEY, AWS_SECRET_KEY

def ec2_security_check(instances_by_region):
    """
    Assess EC2 instances for potential misconfigurations or security risks.
    Processes all instances by region and updates them with any issues found, along with risk tags.
    """
    for region, reservations in instances_by_region.items():
        for reservation in reservations:
            for instance in reservation.get("Instances", []):
                security_groups = instance.get("SecurityGroups", [])
                issues = []

                # Extract security group IDs
                group_ids = [sg['GroupId'] for sg in security_groups]

                # Fetch details for these security groups
                security_group_details = get_security_group_details(region, group_ids)

                # Check for misconfigurations
                for sg_detail in security_group_details:
                    for ip_permission in sg_detail.get("IpPermissions", []):
                        for ip_range in ip_permission.get("IpRanges", []):
                            if ip_range.get("CidrIp") == "0.0.0.0/0":
                                issues.append({
                                    "Issue": f"Security group {sg_detail['GroupId']} allows public access on port "
                                             f"{ip_permission.get('FromPort', 'unknown')}.",
                                    "RiskTags": ["PublicAccess", "NetworkExposure", "HighRisk"]
                                })

                # Check if instance metadata version 1 is allowed (CIS 1.5)
                if instance.get("MetadataOptions", {}).get("HttpTokens", "optional") != "required":
                    issues.append({
                        "Issue": f"EC2 instance {instance['InstanceId']} allows HTTP metadata v1 access.",
                        "RiskTags": ["MetadataAccess", "InformationDisclosure", "MediumRisk"]
                    })

                # Check if instance is not using encryption (CIS 3.4, NIST SC-13)
                if not instance.get("BlockDeviceMappings"):
                    issues.append({
                        "Issue": f"EC2 instance {instance['InstanceId']} does not have encrypted EBS volumes.",
                        "RiskTags": ["DataEncryption", "DataAtRest", "CriticalRisk"]
                    })

                # Attach issues to the instance
                instance["Issues"] = issues

    return instances_by_region

def get_security_group_details(region, group_ids=None):
    """
    Fetch details for specific security groups or all security groups in the given region.
    """
    try:
        ec2_client = boto3.client(
            'ec2',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name=region,
        )
        if group_ids:
            response = ec2_client.describe_security_groups(GroupIds=group_ids)
        else:
            response = ec2_client.describe_security_groups()
        return response['SecurityGroups']
    except Exception as e:
        raise Exception(f"Error fetching security groups in region {region}: {str(e)}")
