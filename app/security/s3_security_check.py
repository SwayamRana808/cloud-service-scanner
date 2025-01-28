import boto3
from app.config import AWS_ACCESS_KEY, AWS_SECRET_KEY
from botocore.exceptions import ClientError

def s3_security_check(buckets):
    """
    Assess S3 buckets for potential misconfigurations or security risks.
    Adds categorized Risk Tags for each identified issue.
    """
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
    )

    detailed_buckets = []

    for bucket in buckets:
        bucket_name = bucket['Name']
        bucket_detail = {
            "Name": bucket_name,
            "CreationDate": bucket['CreationDate'],
        }

        try:
            region_info = s3_client.get_bucket_location(Bucket=bucket_name)
            bucket_region = region_info.get('LocationConstraint', 'us-east-1')
            bucket_detail["Region"] = bucket_region

            bucket_detail["PublicAccessBlockConfiguration"] = s3_client.get_public_access_block(
                Bucket=bucket_name
            ).get('PublicAccessBlockConfiguration', {})

            bucket_detail["Encryption"] = s3_client.get_bucket_encryption(
                Bucket=bucket_name
            )

            try:
                bucket_policy = s3_client.get_bucket_policy(Bucket=bucket_name)
                bucket_detail["BucketPolicy"] = bucket_policy.get("Policy", {})
            except ClientError:
                bucket_detail["BucketPolicy"] = {}

        except ClientError as e:
            bucket_detail["Error"] = str(e)

        issues = []

        # Check for public ACLs (CIS 2.3, PCI DSS 2.2.3)
        if bucket_detail.get('PublicAccessBlockConfiguration', {}).get('BlockPublicAcls', True) is False:
            issues.append({
                "Issue": f"S3 Bucket {bucket_name} has public ACLs enabled.",
                "RiskTags": ["PublicAccess", "ACLConfiguration", "HighRisk"]
            })

        # Check for encryption (CIS 2.6, PCI DSS 3.4.1)
        if not bucket_detail.get('Encryption', {}).get('ServerSideEncryptionConfiguration', {}):
            issues.append({
                "Issue": f"S3 Bucket {bucket_name} does not have server-side encryption enabled.",
                "RiskTags": ["Encryption", "DataProtection", "HighRisk"]
            })

        # Check bucket policy for issues (CIS 2.7, PCI DSS 2.2.3)
        bucket_policy = bucket_detail.get("BucketPolicy", {})
        if isinstance(bucket_policy, dict):
            if "Principal" in bucket_policy and bucket_policy["Principal"] == "*":
                issues.append({
                    "Issue": f"S3 Bucket {bucket_name} has a policy allowing unrestricted access (Principal: *).",
                    "RiskTags": ["PublicAccess", "Policy", "HighRisk"]
                })

            if "Action" in bucket_policy and "*" in bucket_policy["Action"]:
                issues.append({
                    "Issue": f"S3 Bucket {bucket_name} policy allows unrestricted actions (Action: *).",
                    "RiskTags": ["PolicyMisconfiguration", "HighRisk"]
                })

            if any(action in ["s3:GetObject", "s3:ListBucket"] for action in bucket_policy.get("Action", [])):
                issues.append({
                    "Issue": f"S3 Bucket {bucket_name} policy allows public access via GET or LIST actions.",
                    "RiskTags": ["PublicAccess", "Policy", "HighRisk"]
                })

        else:
            issues.append({
                "Issue": f"S3 Bucket {bucket_name} has an invalid policy format.",
                "RiskTags": ["PolicyMisconfiguration", "MediumRisk"]
            })

        bucket_detail["Issues"] = issues
        detailed_buckets.append(bucket_detail)

    return detailed_buckets
