import allure

from selenium.webdriver.support import expected_conditions as EC

from .base_page import BasePage
from .locators import OrdersFeedPageLocators


class OrdersFeedPage(BasePage):

    @allure.step("Проверить, что лента заказов видна")
    def is_feed_visible(self):
        self.find(OrdersFeedPageLocators.FEED_SECTION)
        return True

    @allure.step("Получить число «Выполнено за все время»")
    def get_total_done(self) -> int:
        self.find(OrdersFeedPageLocators.FEED_SECTION)
        self.find(OrdersFeedPageLocators.DONE_TOTAL_WRAPPER)
        text = self.get_text(OrdersFeedPageLocators.DONE_TOTAL_NUMBER)
        return int(text.replace(" ", "")) if text else 0

    @allure.step("Получить число «Выполнено за сегодня»")
    def get_today_done(self) -> int:
        self.find(OrdersFeedPageLocators.FEED_SECTION)
        self.find(OrdersFeedPageLocators.DONE_TODAY_WRAPPER)
        text = self.get_text(OrdersFeedPageLocators.DONE_TODAY_NUMBER)
        return int(text.replace(" ", "")) if text else 0

    @allure.step("Получить список номеров заказов в разделе «В работе»")
    def get_in_progress_numbers(self) -> list[str]:
        self.find(OrdersFeedPageLocators.FEED_SECTION)
        self.find(OrdersFeedPageLocators.STATUS_BOX)
        self.find(OrdersFeedPageLocators.IN_PROGRESS_LIST)

        self.wait.until(
            EC.presence_of_all_elements_located(
                OrdersFeedPageLocators.IN_PROGRESS_ITEMS
            )
        )

        def _has_real_numbers(driver):
            elements = driver.find_elements(*OrdersFeedPageLocators.IN_PROGRESS_ITEMS)
            for el in elements:
                text = el.text.strip()
                if text and text != "Все текущие заказы готовы!":
                    return True
            return False

        self.wait.until(_has_real_numbers)

        elements = self.find_all(OrdersFeedPageLocators.IN_PROGRESS_ITEMS)
        numbers: list[str] = []
        for el in elements:
            text = el.text.strip()
            if text and text != "Все текущие заказы готовы!":
                normalized = text.lstrip("0")
                numbers.append(normalized)
        return numbers