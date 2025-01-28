# services_risk_counter.py

def count_ec2_risks(ec2_data):
    highRisk = 0
    mediumRisk = 0
    lowRisk = 0
    
    for region, reservations in ec2_data.items():
        for reservation in reservations:
            for instance in reservation['Instances']:
                if instance.get('Issues'):
                    for issue in instance['Issues']:
                        if 'HighRisk' in issue['RiskTags']:
                            highRisk += 1
                        elif 'MediumRisk' in issue['RiskTags']:
                            mediumRisk += 1
                        else:
                            lowRisk += 1
    return highRisk, mediumRisk, lowRisk


def count_s3_risks(s3_data):
    # Implement S3-specific logic here
    highRisk = 0
    mediumRisk = 0
    lowRisk = 0
    # For example:
    for bucket in s3_data.get('Buckets', []):
        if 'Issues' in bucket:
            for issue in bucket['Issues']:
                if 'HighRisk' in issue['RiskTags']:
                    highRisk += 1
                elif 'MediumRisk' in issue['RiskTags']:
                    mediumRisk += 1
                else:
                    lowRisk += 1
    return highRisk, mediumRisk, lowRisk


def count_iam_risks(iam_data):
    # Implement IAM-specific logic here
    highRisk = 0
    mediumRisk = 0
    lowRisk = 0
    for user in iam_data.get('Users', []):
        if 'Issues' in user:
            for issue in user['Issues']:
                if 'HighRisk' in issue['RiskTags']:
                    highRisk += 1
                elif 'MediumRisk' in issue['RiskTags']:
                    mediumRisk += 1
                else:
                    lowRisk += 1
    return highRisk, mediumRisk, lowRisk


# Add more services here as needed, like RDS, NACL, Security Groups, etc.
