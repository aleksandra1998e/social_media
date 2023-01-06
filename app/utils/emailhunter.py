import requests


def verify_email(email: str):
    """Verify email using EmailHunter API"""
    response = requests.get(f"https://api.emailhunter.co/v1/verify?email={email}&api_key=your_api_key")
    return response.json()
