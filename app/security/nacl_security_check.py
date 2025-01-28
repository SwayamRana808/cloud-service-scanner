def analyze_network_acls(nacls):
    """
    Analyze Network ACLs (NACLs) for potential security issues.
    Each issue is categorized with associated risk tags.
    """
    for nacl in nacls:
        issues = []
        nacl_id = nacl.get("NetworkAclId")
        entries = nacl.get("Entries", [])
        is_default = nacl.get("IsDefault", False)
        associated_subnets = [
            association.get("SubnetId") for association in nacl.get("Associations", [])
        ]

        for entry in entries:
            cidr_block = entry.get("CidrBlock")
            rule_action = entry.get("RuleAction")
            protocol = entry.get("Protocol")
            egress = entry.get("Egress")
            port_range = entry.get("PortRange", {})

            # Check for overly permissive rules
            if cidr_block == "0.0.0.0/0" and rule_action == "allow":
                issues.append({
                    "Issue": (
                        f"NACL {nacl_id} allows unrestricted {'outbound' if egress else 'inbound'} "
                        f"access ({'egress' if egress else 'ingress'} rule). Protocol: {protocol}, "
                        f"Port Range: {port_range.get('From', 'any')} - {port_range.get('To', 'any')}."
                    ),
                    "RiskTags": ["OverlyPermissive", "NetworkAccessControl", "HighRisk"]
                })

        # Check if the NACL is the default one (optional informational tag)
        if is_default:
            issues.append({
                "Issue": f"NACL {nacl_id} is a default NACL, which might require stricter rule management.",
                "RiskTags": ["DefaultNACL", "Configuration", "MediumRisk"]
            })

        # Add issues to the NACL object
        nacl["Issues"] = issues

    return nacls
