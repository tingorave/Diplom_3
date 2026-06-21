from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url: str):
        self.driver.get(url)

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def finds(self, locator):
        """Вернуть все видимые элементы по локатору (старое имя)."""
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def find_all(self, locator):
        """
        Вернуть список всех элементов по локатору.
        Совместимо с вызовами find_all(...) в страницах.
        """
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def get_text(self, locator) -> str:
        return self.find(locator).text