from selenium.webdriver.common.by import By


class MainPageLocators:
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

    # Оверлей модалки (важно: просто div, не внутри section)
    MODAL_OVERLAY = (
        By.CSS_SELECTOR,
        "div.Modal_modal_overlay__x2ZCr",
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


class OrdersFeedPageLocators:
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