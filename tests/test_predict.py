from src.predict import suspicious_terms


def test_suspicious_terms_detects_healthcare_scam_language():
    terms = suspicious_terms("Urgent Medicare card verification: send SSN and OTP now")
    assert "urgent" in terms
    assert "ssn" in terms
    assert "otp" in terms
