import requests


def get_user_info(email: str):
    """Get user info from Clearbit API"""
    response = requests.get(f"https://person.clearbit.com/v2/people/email/{email}",
                            auth=("sk_your_api_key", ""))
    return response.json()


def get_company_info(domain: str):
    """Get company info from Clearbit API"""
    response = requests.get(f"https://company.clearbit.com/v2/companies/domain/{domain}",
                            auth=("sk_your_api_key", ""))
    return response.json()
