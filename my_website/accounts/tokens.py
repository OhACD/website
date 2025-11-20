from django.core import signing
import time

def generate_login_token(data: dict, expires=1800):
    data['exp'] = time.time() + expires
    return signing.dumps(data, salt="magic-link")

def generate_verification_token(data: dict, expires=60 * 60 * 24):
    data['exp'] = time.time() + expires
    return signing.dumps(data, salt="magic-link")


def verify_login_token(token, max_age=1800):
    try:
        data = signing.loads(token, salt="magic-link", max_age=max_age)
        if data.get('exp', 0) < time.time():
            return None
        return data
    except Exception:
        return None

def verify_verification_token(token, max_age=60*60*24):
    try:
        data = signing.loads(token, salt="magic-link", max_age=max_age)
        if data.get('exp', 0) < time.time():
            return None
        return data
    except Exception:
        return None
