import re

EMAIL_REGEX = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

def is_valid_email(email: str) -> bool:
    if not email:
        return False
    return re.match(EMAIL_REGEX, email) is not None
