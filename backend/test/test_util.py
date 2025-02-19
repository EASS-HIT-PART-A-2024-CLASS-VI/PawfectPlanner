from app.util import validate_email, parse_date

class TestUtils:
    """
    Tests for utility functions.
    """

    def test_validate_email_valid(self):
        """
        Test validating a correct email.
        """
        assert validate_email("test@example.com") is True

    def test_validate_email_invalid(self):
        """
        Test validating an incorrect email.
        """
        assert validate_email("not-an-email") is False

    def test_parse_date_valid(self):
        """
        Test parsing a valid date.
        """
        assert parse_date("2024-01-30") == "2024-01-30"

    def test_parse_date_invalid(self):
        """
        Test parsing an invalid date.
        """
        assert parse_date("invalid-date") is None
