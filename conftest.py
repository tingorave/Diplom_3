import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from pages.config import BASE_URL


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    browser = request.param

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)

    else:
        raise ValueError(f"Unknown browser: {browser}")

    driver.maximize_window()
    driver.implicitly_wait(5)

    yield driver

    driver.quit()


@pytest.fixture
def authorized_driver(driver):
    """
    Драйвер с уже авторизованным пользователем через API.
    Используем в UI-тестах, где не проверяется форма логина.
    """
    email = "valentin_mikhanosha_sprint5@yandex.ru"
    password = "Qwerty123"

    url = f"{BASE_URL}/api/auth/login"
    resp = requests.post(url, json={"email": email, "password": password})
    resp.raise_for_status()
    data = resp.json()

    access = data.get("accessToken", "")
    refresh = data.get("refreshToken", "")

    if access.startswith("Bearer "):
        access = access[len("Bearer "):]

    driver.get(BASE_URL)

    driver.execute_script(
        "window.localStorage.setItem(arguments[0], arguments[1]);",
        "accessToken",
        f"Bearer {access}",
    )
    driver.execute_script(
        "window.localStorage.setItem(arguments[0], arguments[1]);",
        "refreshToken",
        refresh,
    )

    driver.refresh()

    return driver