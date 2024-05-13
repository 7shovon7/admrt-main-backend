def generate_username_from_email(email: str):
    return email.strip().lower().replace('@', '_')
