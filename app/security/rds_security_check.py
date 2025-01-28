def rds_security_check(instances_by_region):
    """
    Assess RDS instances for potential misconfigurations or security risks.
    Adds categorized Risk Tags for each identified issue.
    """
    for region, instances in instances_by_region.items():
        for instance in instances:
            issues = []

            # Check for public accessibility (CIS 5.1, PCI DSS 2.2.3)
            if instance.get('PubliclyAccessible', False):
                issues.append({
                    "Issue": f"RDS instance {instance['DBInstanceIdentifier']} is publicly accessible.",
                    "RiskTags": ["PublicAccess", "Configuration", "HighRisk"]
                })

            # Check for backup configuration (CIS 5.6, NIST CP-9)
            if instance.get('BackupRetentionPeriod', 0) == 0:
                issues.append({
                    "Issue": f"RDS instance {instance['DBInstanceIdentifier']} does not have backups enabled.",
                    "RiskTags": ["DataProtection", "Configuration", "MediumRisk"]
                })

            # Check for Multi-AZ deployment (CIS 5.7)
            if not instance.get('MultiAZ', False):
                issues.append({
                    "Issue": f"RDS instance {instance['DBInstanceIdentifier']} is not configured for Multi-AZ deployment.",
                    "RiskTags": ["HighAvailability", "Configuration", "MediumRisk"]
                })

            # Ensure encryption is enabled for RDS (NIST SC-13, PCI DSS 3.4.1)
            if not instance.get('StorageEncrypted', False):
                issues.append({
                    "Issue": f"RDS instance {instance['DBInstanceIdentifier']} does not have encryption enabled.",
                    "RiskTags": ["Encryption", "DataProtection", "HighRisk"]
                })

            instance["Issues"] = issues

    return instances_by_region
