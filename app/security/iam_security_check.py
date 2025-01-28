import boto3
from app.config import AWS_ACCESS_KEY, AWS_SECRET_KEY

def iam_security_check(users):
    """
    Assess IAM users for potential misconfigurations or security risks.
    Each issue is categorized with associated risk tags.
    """
    iam_client = boto3.client('iam', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

    for user in users:
        issues = []

        # Fetch Access Key Last Used Information
        try:
            access_key_last_used = iam_client.get_user(UserName=user['UserName']).get('User', {}).get('AccessKeyLastUsed')
            if access_key_last_used and not user.get('PasswordLastUsed'):
                issues.append({
                    "Issue": f"IAM User {user['UserName']} has never logged in but has active access keys.",
                    "RiskTags": ["InactiveUser", "AccessKeyManagement", "MediumRisk"]
                })
        except Exception as e:
            issues.append({
                "Issue": f"Error fetching access key last used for user {user['UserName']}: {str(e)}",
                "RiskTags": ["Error", "Monitoring"]
            })

        # Check Access Keys Status
        try:
            access_keys = iam_client.list_access_keys(UserName=user['UserName'])['AccessKeyMetadata']
            for key in access_keys:
                if key.get('Status') == 'Inactive':
                    issues.append({
                        "Issue": f"Access key {key['AccessKeyId']} for user {user['UserName']} is inactive but not deleted.",
                        "RiskTags": ["InactiveKey", "AccessKeyManagement", "LowRisk"]
                    })
        except Exception as e:
            issues.append({
                "Issue": f"Error fetching access keys for user {user['UserName']}: {str(e)}",
                "RiskTags": ["Error", "Monitoring"]
            })

        # Check for MFA Devices
        try:
            mfa_devices = iam_client.list_mfa_devices(UserName=user['UserName'])['MFADevices']
            if not mfa_devices:
                issues.append({
                    "Issue": f"IAM User {user['UserName']} does not have MFA enabled.",
                    "RiskTags": ["MFA", "Authentication", "HighRisk"]
                })
        except Exception as e:
            issues.append({
                "Issue": f"Error fetching MFA devices for user {user['UserName']}: {str(e)}",
                "RiskTags": ["Error", "Authentication"]
            })

        # Ensure user is not an administrator (CIS 1.5)
        try:
            user_policies = iam_client.list_attached_user_policies(UserName=user['UserName'])['AttachedPolicies']
            for policy in user_policies:
                if 'Administrator' in policy['PolicyName']:
                    issues.append({
                        "Issue": f"IAM User {user['UserName']} has administrator access, violating least privilege.",
                        "RiskTags": ["LeastPrivilege", "PolicyManagement", "CriticalRisk"]
                    })
        except Exception as e:
            issues.append({
                "Issue": f"Error checking attached policies for user {user['UserName']}: {str(e)}",
                "RiskTags": ["Error", "PolicyManagement"]
            })

        # Attach issues to the user
        user["Issues"] = issues

    return users
