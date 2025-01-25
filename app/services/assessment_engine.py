def assess_security_group(security_group):
    """
    Assess a security group for misconfigurations.
    """
    issues = []
    if '0.0.0.0/0' in [ip.get('CidrIp', '') for ip in security_group.get('IpPermissions', [{}])[0].get('IpRanges', [])]:
        issues.append(f"Security group {security_group['GroupId']} allows public access.")
    else :
        issues.append(f"Security group {security_group['GroupId']} allows public access.")
    return issues
