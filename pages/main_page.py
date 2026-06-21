import time

from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

from .base_page import BasePage


BASE_URL = "https://stellarburgers.education-services.ru"


class MainPage(BasePage):
    # Вкладки в шапке
    CONSTRUCTOR_TAB = (
        By.XPATH,
        "//a[contains(@class,'AppHeader_header__link')][.//p[text()='Конструктор']]",
    )
    FEED_TAB = (
        By.XPATH,
        "//a[contains(@class,'AppHeader_header__link')][.//p[text()='Лента Заказов']]",
    )

    # Заголовки секций
    CONSTRUCTOR_SECTION = (By.XPATH, "//h1[text()='Соберите бургер']")
    FEED_SECTION = (By.XPATH, "//h1[text()='Лента заказов']")

    # Первая карточка ингредиента
    FIRST_INGREDIENT_CARD = (
        By.CSS_SELECTOR,
        "a.BurgerIngredient_ingredient__1TVf6",
    )

    # Счётчик на первой карточке ингредиента
    FIRST_INGREDIENT_COUNTER = (
        By.CSS_SELECTOR,
        "a.BurgerIngredient_ingredient__1TVf6 p.counter_counter__num__3nue1",
    )

    # Область конструктора
    CONSTRUCTOR_DROP_AREA = (
        By.CSS_SELECTOR,
        "section.BurgerConstructor_basket__29Cd7",
    )

    # Сумма заказа
    ORDER_TOTAL = (
        By.CSS_SELECTOR,
        "section.BurgerConstructor_basket__29Cd7 "
        "div.BurgerConstructor_basket__totalContainer__2Z-ho p.text_type_digits-medium",
    )

    # Кнопка оформления заказа
    ORDER_BUTTON = (
        By.XPATH,
        "//button[contains(@class,'button_button_type_primary__1O7Bx')"
        " and contains(., 'Оформить заказ')]",
    )

    # ---------- авторизация ----------

    LOGIN_HEADER_BUTTON = (
        By.XPATH,
        "//button[contains(., 'Войти в аккаунт')]",
    )

    EMAIL_INPUT = (
        By.XPATH,
        "//label[text()='Email']/following-sibling::input",
    )
    PASSWORD_INPUT = (
        By.XPATH,
        "//label[text()='Пароль']/following-sibling::input",
    )
    SUBMIT_LOGIN_BUTTON = (
        By.XPATH,
        "//button[contains(@class,'button_button_type_primary__1O7Bx') and text()='Войти']",
    )

    # Модальное окно заказа
    ORDER_MODAL_SECTION = (
        By.CSS_SELECTOR,
        "section.Modal_modal__P3_V5",
    )

    # Оверлей модалки
    MODAL_OVERLAY = (
        By.CSS_SELECTOR,
        "section.Modal_modal__P3_V5 div.Modal_modal_overlay__x2ZCr",
    )

    # Кнопка закрытия модалки (крестик)
    MODAL_CLOSE_BUTTON = (
        By.CSS_SELECTOR,
        "section.Modal_modal__P3_V5 button.Modal_modal__close__TnseK",
    )

    # Номер заказа в модалке (h2)
    ORDER_NUMBER_IN_MODAL = (
        By.XPATH,
        "//section[contains(@class,'Modal_modal__P3_V5')]"
        "//h2[contains(@class,'Modal_modal__title__2L34m')]",
    )

    def open_main(self):
        self.open(BASE_URL)

    def go_to_constructor(self):
        self.click(self.CONSTRUCTOR_TAB)

    def go_to_feed(self):
        """Перейти в ленту заказов после полного закрытия модалки."""
        from .orders_feed_page import OrdersFeedPage

        # Ждём, что overlay исчез
        try:
            self.wait.until(
                EC.invisibility_of_element_located(self.MODAL_OVERLAY)
            )
        except Exception:
            pass

        self.click(self.FEED_TAB)
        feed_page = OrdersFeedPage(self.driver)
        feed_page.is_feed_visible()

    def is_constructor_visible(self):
        self.find(self.CONSTRUCTOR_SECTION)
        return True

    def is_feed_visible(self):
        self.find(self.FEED_SECTION)
        return True

    def open_first_ingredient(self):
        self.click(self.FIRST_INGREDIENT_CARD)

    def is_ingredient_modal_open(self):
        self.find(self.ORDER_MODAL_SECTION)
        return True

    def close_ingredient_modal(self):
        """Закрыть модалку ингредиента кликом по крестику и дождаться исчезновения."""
        close_btn = self.wait.until(
            EC.element_to_be_clickable(self.MODAL_CLOSE_BUTTON)
        )
        close_btn.click()

        try:
            self.wait.until(
                EC.invisibility_of_element_located(self.MODAL_OVERLAY)
            )
        except Exception:
            pass

    def close_modal(self):
        """Закрыть модалку заказа кликом по крестику и дождаться исчезновения overlay."""
        close_btn = self.wait.until(
            EC.element_to_be_clickable(self.MODAL_CLOSE_BUTTON)
        )
        close_btn.click()

        # Ждём, пока overlay полностью исчезнет
        try:
            self.wait.until(
                EC.invisibility_of_element_located(self.MODAL_OVERLAY)
            )
        except Exception:
            pass

    def get_first_ingredient_counter(self):
        text = self.get_text(self.FIRST_INGREDIENT_COUNTER)
        return int(text) if text else 0

    def drag_first_ingredient_to_constructor(self):
        source = self.find(self.FIRST_INGREDIENT_CARD)
        target = self.find(self.CONSTRUCTOR_DROP_AREA)
        actions = ActionChains(self.driver)
        actions.drag_and_drop(source, target).perform()

    def get_order_total(self):
        text = self.get_text(self.ORDER_TOTAL)
        return int(text) if text else 0

    def click_order_button(self):
        """Клик по кнопке «Оформить заказ»."""
        self.click(self.ORDER_BUTTON)

    def wait_for_order_modal(self, timeout: int = 20):
        """
        Ожидать:
        1) появления заголовка с номером заказа;
        2) пока в нём появится корректный номер:
           - только цифры,
           - длина 6 символов,
           - не '9999'.
        """
        # 1. Ждём появления самого заголовка
        title_elem = self.wait.until(
            EC.visibility_of_element_located(self.ORDER_NUMBER_IN_MODAL)
        )

        # 2. Ждём, пока текст станет корректным номером
        start = time.time()
        while True:
            text = title_elem.text.strip()
            # защищаемся от первоначального фейкового значения 9999
            if (
                text
                and text.isdigit()
                and len(text) == 6
                and text != "9999"
            ):
                break

            if time.time() - start > timeout:
                raise TimeoutException(
                    f"Корректный номер заказа не появился в модалке за {timeout} сек, текущее значение: {text!r}"
                )
            time.sleep(0.3)

        return title_elem

    def get_order_number_from_modal(self):
        text = self.get_text(self.ORDER_NUMBER_IN_MODAL)
        return text.strip()

    def login(self, email: str, password: str):
        """Авторизация пользователя через кнопку 'Войти в аккаунт'."""
        self.click(self.LOGIN_HEADER_BUTTON)

        email_input = self.find(self.EMAIL_INPUT)
        password_input = self.find(self.PASSWORD_INPUT)

        email_input.clear()
        email_input.send_keys(email)
        password_input.clear()
        password_input.send_keys(password)

        self.click(self.SUBMIT_LOGIN_BUTTON)
        self.find(self.CONSTRUCTOR_SECTION)