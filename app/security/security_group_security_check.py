def analyze_security_groups(security_group):
    """
    Analyze a single security group for potential misconfigurations.
    Returns a list of issues with categorized risk tags.
    """
    issues = []

    # Analyze inbound rules
    for rule in security_group.get("IpPermissions", []):
        for ip_range in rule.get("IpRanges", []):
            if ip_range.get("CidrIp") == "0.0.0.0/0":
                issues.append({
                    "Issue": f"Inbound rule allows unrestricted access: Protocol: {rule.get('IpProtocol')}, "
                             f"Ports: {rule.get('FromPort', 'unknown')} - {rule.get('ToPort', 'unknown')}.",
                    "RiskTags": ["PublicAccess", "InboundRule", "HighRisk"]
                })

    # Analyze outbound rules
    for rule in security_group.get("IpPermissionsEgress", []):
        for ip_range in rule.get("IpRanges", []):
            if ip_range.get("CidrIp") == "0.0.0.0/0":
                issues.append({
                    "Issue": f"Outbound rule allows unrestricted access: Protocol: {rule.get('IpProtocol')}.",
                    "RiskTags": ["PublicAccess", "OutboundRule", "MediumRisk"]
                })

    return issues
