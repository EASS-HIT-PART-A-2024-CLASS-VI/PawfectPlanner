import pytest
from backend.app.util import validate_email, parse_date

def test_validate_email():
    assert validate_email("test@example.com") is True
    assert validate_email("invalid-email") is False

def test_parse_date():
    assert parse_date("2023-12-01") == "2023-12-01"
    with pytest.raises(ValueError):
        parse_date("invalid-date")
