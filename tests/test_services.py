import pytest
from app.services.misconfig_detection import assess_security_group

def test_assess_security_group():
    test_group = {"IpPermissions": ["0.0.0.0/0"]}
    result = assess_security_group(test_group)
    assert result['issue'] == "Security group is open to the world"
    assert result['severity'] == "high"
