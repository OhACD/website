from django.core import signing

def generate_token(data: dict, expires=3600):
    return signing.dumps(data, salt="magic-link")

def verify_token(token, max_age=3600):
    try:
        return signing.loads(token, salt="magic-link", max_age=max_age)
    except Exception:
        return None
