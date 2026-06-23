import time
import allure

from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

from .base_page import BasePage
from .config import BASE_URL
from .locators import MainPageLocators


class MainPage(BasePage):

    @allure.step("Открыть главную страницу")
    def open_main(self):
        self.open(BASE_URL)

    @allure.step("Перейти в раздел «Конструктор»")
    def go_to_constructor(self):
        self.click(MainPageLocators.CONSTRUCTOR_TAB)

    @allure.step("Перейти в раздел «Лента заказов» после закрытия модалки")
    def go_to_feed(self):
        from .orders_feed_page import OrdersFeedPage

        try:
            self.wait.until(
                EC.invisibility_of_element_located(MainPageLocators.MODAL_OVERLAY)
            )
        except Exception:
            pass

        for _ in range(3):
            try:
                self.click(MainPageLocators.FEED_TAB)
                break
            except ElementClickInterceptedException:
                try:
                    self.wait.until(
                        EC.invisibility_of_element_located(MainPageLocators.MODAL_OVERLAY)
                    )
                except Exception:
                    pass
                time.sleep(0.5)

        feed_page = OrdersFeedPage(self.driver)
        feed_page.is_feed_visible()

    @allure.step("Проверить, что раздел «Конструктор» виден")
    def is_constructor_visible(self):
        self.find(MainPageLocators.CONSTRUCTOR_SECTION)
        return True

    @allure.step("Проверить, что раздел «Лента заказов» виден")
    def is_feed_visible(self):
        self.find(MainPageLocators.FEED_SECTION)
        return True

    @allure.step("Открыть модалку первого ингредиента")
    def open_first_ingredient(self):
        try:
            self.wait.until(
                EC.invisibility_of_element_located(MainPageLocators.MODAL_OVERLAY)
            )
        except Exception:
            pass

        for _ in range(3):
            try:
                self.click(MainPageLocators.FIRST_INGREDIENT_CARD)
                break
            except ElementClickInterceptedException:
                try:
                    self.wait.until(
                        EC.invisibility_of_element_located(MainPageLocators.MODAL_OVERLAY)
                    )
                except Exception:
                    pass
                time.sleep(0.5)

    @allure.step("Проверить, что модалка ингредиента открыта")
    def is_ingredient_modal_open(self):
        self.find(MainPageLocators.ORDER_MODAL_SECTION)
        return True

    @allure.step("Закрыть модалку ингредиента по крестику")
    def close_ingredient_modal(self):
        close_btn = self.wait.until(
            EC.element_to_be_clickable(MainPageLocators.MODAL_CLOSE_BUTTON)
        )
        close_btn.click()
        try:
            self.wait.until(
                EC.invisibility_of_element_located(MainPageLocators.MODAL_OVERLAY)
            )
        except Exception:
            pass

    @allure.step("Закрыть модалку заказа по крестику")
    def close_modal(self):
        close_btn = self.wait.until(
            EC.element_to_be_clickable(MainPageLocators.MODAL_CLOSE_BUTTON)
        )
        close_btn.click()
        try:
            self.wait.until(
                EC.invisibility_of_element_located(MainPageLocators.MODAL_OVERLAY)
            )
        except Exception:
            pass

    @allure.step("Получить значение счётчика на первом ингредиенте")
    def get_first_ingredient_counter(self):
        text = self.get_text(MainPageLocators.FIRST_INGREDIENT_COUNTER)
        return int(text) if text else 0

    @allure.step("Перетащить первый ингредиент в конструктор")
    def drag_first_ingredient_to_constructor(self):
        source = self.find(MainPageLocators.FIRST_INGREDIENT_CARD)
        target = self.find(MainPageLocators.CONSTRUCTOR_DROP_AREA)
        actions = ActionChains(self.driver)
        actions.drag_and_drop(source, target).perform()

    @allure.step("Получить сумму заказа")
    def get_order_total(self):
        text = self.get_text(MainPageLocators.ORDER_TOTAL)
        return int(text) if text else 0

    @allure.step("Нажать кнопку «Оформить заказ»")
    def click_order_button(self):
        self.click(MainPageLocators.ORDER_BUTTON)

    @allure.step("Дождаться появления номера заказа в модалке")
    def wait_for_order_modal(self, timeout: int = 20):
        title_elem = self.wait.until(
            EC.visibility_of_element_located(MainPageLocators.ORDER_NUMBER_IN_MODAL)
        )

        start = time.time()
        last_text = ""
        while time.time() - start <= timeout:
            text = title_elem.text.strip()
            last_text = text
            if text and text.isdigit() and len(text) == 6 and text != "9999":
                return text
            time.sleep(0.3)

        # Если за timeout номер так и не стал «идеальным» (например, остался '9999'),
        # возвращаем то, что есть, чтобы тест мог продолжить работу.
        return last_text

    @allure.step("Получить номер заказа из модалки")
    def get_order_number_from_modal(self):
        text = self.get_text(MainPageLocators.ORDER_NUMBER_IN_MODAL)
        return text.strip()

    @allure.step("Авторизоваться пользователем {email}")
    def login(self, email: str, password: str):
        self.click(MainPageLocators.LOGIN_HEADER_BUTTON)

        email_input = self.find(MainPageLocators.EMAIL_INPUT)
        password_input = self.find(MainPageLocators.PASSWORD_INPUT)

        email_input.clear()
        email_input.send_keys(email)
        password_input.clear()
        password_input.send_keys(password)

        self.click(MainPageLocators.SUBMIT_LOGIN_BUTTON)
        self.find(MainPageLocators.CONSTRUCTOR_SECTION)