from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from .base_page import BasePage


class OrdersFeedPage(BasePage):

    # Заголовок секции «Лента заказов»
    FEED_SECTION = (By.XPATH, "//h1[text()='Лента заказов']")

    # Колонка статусов (Готовы / В работе)
    STATUS_BOX = (
        By.CSS_SELECTOR,
        "div.OrderFeed_orderStatusBox__1d4q2",
    )

    # Список номеров в разделе «В работе»
    IN_PROGRESS_LIST = (
        By.CSS_SELECTOR,
        "div.OrderFeed_orderStatusBox__1d4q2 ul.OrderFeed_orderList__cBvyi",
    )

    # Элементы-номера заказов в «В работе»
    IN_PROGRESS_ITEMS = (
        By.CSS_SELECTOR,
        "div.OrderFeed_orderStatusBox__1d4q2 ul.OrderFeed_orderList__cBvyi li.text.text_type_digits-default.mb-2",
    )

    # Блок «Выполнено за всё время»
    DONE_TOTAL_WRAPPER = (
        By.XPATH,
        "//p[text()='Выполнено за все время:']/parent::div",
    )
    DONE_TOTAL_NUMBER = (
        By.XPATH,
        "//p[text()='Выполнено за все время:']/following-sibling::p[contains(@class,'OrderFeed_number__')]",
    )

    # Блок «Выполнено за сегодня»
    DONE_TODAY_WRAPPER = (
        By.XPATH,
        "//p[text()='Выполнено за сегодня:']/parent::div",
    )
    DONE_TODAY_NUMBER = (
        By.XPATH,
        "//p[text()='Выполнено за сегодня:']/following-sibling::p[contains(@class,'OrderFeed_number__')]",
    )

    def is_feed_visible(self):
        self.find(self.FEED_SECTION)
        return True

    def get_total_done(self) -> int:
        """Получить число «Выполнено за все время»."""
        self.find(self.FEED_SECTION)
        self.find(self.DONE_TOTAL_WRAPPER)
        text = self.get_text(self.DONE_TOTAL_NUMBER)
        return int(text.replace(" ", "")) if text else 0

    def get_today_done(self) -> int:
        """Получить число «Выполнено за сегодня»."""
        self.find(self.FEED_SECTION)
        self.find(self.DONE_TODAY_WRAPPER)
        text = self.get_text(self.DONE_TODAY_NUMBER)
        return int(text.replace(" ", "")) if text else 0

    def get_in_progress_numbers(self) -> list[str]:
        """
        Получить список номеров заказов в разделе «В работе».
        Например: ['0384989', '0384988', ...].
        """
        self.find(self.FEED_SECTION)
        self.find(self.STATUS_BOX)
        self.find(self.IN_PROGRESS_LIST)

        # 1. Ждём, пока появятся любые элементы в списке
        self.wait.until(
            EC.presence_of_all_elements_located(self.IN_PROGRESS_ITEMS)
        )

        # 2. Ждём, пока среди них будет хотя бы один НЕ «Все текущие заказы готовы!»
        def _has_real_numbers(driver):
            elements = driver.find_elements(*self.IN_PROGRESS_ITEMS)
            for el in elements:
                text = el.text.strip()
                if text and text != "Все текущие заказы готовы!":
                    return True
            return False

        self.wait.until(_has_real_numbers)

        # 3. Собираем все тексты, отфильтровывая заглушку и убирая ведущие нули
        elements = self.find_all(self.IN_PROGRESS_ITEMS)
        numbers: list[str] = []
        for el in elements:
            text = el.text.strip()
            if text and text != "Все текущие заказы готовы!":
                normalized = text.lstrip("0")
                numbers.append(normalized)
        return numbers