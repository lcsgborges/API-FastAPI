def validate_password(password: str):
    MIN_LENGTH = 8

    has_min_lenght = len(password) >= MIN_LENGTH
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_number = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)

    return all([has_min_lenght, has_lower, has_upper, has_number, has_special])
