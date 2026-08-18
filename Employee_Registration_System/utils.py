import re


def validate_email(email):
    """Validates the format of an email address."""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None


def validate_phone(phone):
    """Validates that a phone number contains only digits and is a reasonable length."""
    return phone.isdigit() and 7 <= len(phone) <= 15
