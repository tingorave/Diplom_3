import allure
from pages.main_page import MainPage


@allure.feature("Навигация и ингредиенты")
class TestNavigation:

    @allure.story("Переход по клику на «Конструктор»")
    def test_go_to_constructor(self, driver):
        page = MainPage(driver)
        page.open_main()
        page.go_to_feed()
        page.go_to_constructor()
        assert page.is_constructor_visible()

    @allure.story("Переход по клику на «Лента заказов»")
    def test_go_to_feed(self, driver):
        page = MainPage(driver)
        page.open_main()
        page.go_to_feed()
        assert page.is_feed_visible()

    @allure.story("Клик по ингредиенту открывает модалку")
    def test_ingredient_modal_open(self, driver):
        page = MainPage(driver)
        page.open_main()
        page.open_first_ingredient()
        assert page.is_ingredient_modal_open()

    @allure.story("Модалка закрывается по крестику")
    def test_ingredient_modal_close(self, driver):
        page = MainPage(driver)
        page.open_main()
        page.open_first_ingredient()
        page.close_ingredient_modal()

    @allure.story("Счётчик ингредиента увеличивается при добавлении в конструктор")
    def test_ingredient_counter_increases(self, driver):
        page = MainPage(driver)
        page.open_main()

        initial = page.get_first_ingredient_counter()
        page.drag_first_ingredient_to_constructor()
        new = page.get_first_ingredient_counter()

        # Для булки добавление даёт +2 (верх и низ)
        assert new == initial + 2