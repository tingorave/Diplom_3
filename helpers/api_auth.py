import requests
from pages.config import BASE_URL


def login_api(email: str, password: str) -> tuple[str, str]:
    """
    Логин по API.
    Возвращает (access_token, refresh_token) без префикса Bearer.
    """
    url = f"{BASE_URL}/api/auth/login"
    resp = requests.post(url, json={"email": email, "password": password})
    resp.raise_for_status()
    data = resp.json()
    
    access = data.get("accessToken", "")
    refresh = data.get("refreshToken", "")

    if access.startswith("Bearer "):
        access = access[len("Bearer "):]

    return access, refresh