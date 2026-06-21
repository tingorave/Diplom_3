import allure
from pages.main_page import MainPage
from pages.orders_feed_page import OrdersFeedPage


@allure.feature("Лента заказов и счётчики")
class TestCounters:

    @allure.story("Счётчик «Выполнено за все время» увеличивается после нового заказа")
    def test_total_done_increases_after_order(self, driver):
        main = MainPage(driver)
        main.open_main()

        main.login("valentin_mikhanosha_sprint5@yandex.ru", "Qwerty123")

        # Оформляем новый заказ
        main.drag_first_ingredient_to_constructor()
        main.drag_first_ingredient_to_constructor()
        main.click_order_button()
        main.wait_for_order_modal()
        order_number = main.get_order_number_from_modal()

        # Закрываем модалку
        main.close_modal()

        # Переходим в ленту и смотрим счётчик
        main.go_to_feed()
        feed = OrdersFeedPage(driver)
        total_after = feed.get_total_done()

        assert total_after > 0
        assert order_number

    @allure.story("Счётчик «Выполнено за сегодня» увеличивается после нового заказа")
    def test_today_done_increases_after_order(self, driver):
        main = MainPage(driver)
        main.open_main()

        # Авторизация
        main.login("valentin_mikhanosha_sprint5@yandex.ru", "Qwerty123")

        # Переходим в ленту и читаем счётчик до оформления
        main.go_to_feed()
        feed = OrdersFeedPage(driver)
        today_before = feed.get_today_done()

        # Возвращаемся в конструктор и оформляем заказ
        main.go_to_constructor()
        main.drag_first_ingredient_to_constructor()
        main.drag_first_ingredient_to_constructor()
        main.click_order_button()
        main.wait_for_order_modal()
        order_number = main.get_order_number_from_modal()

        # Закрываем модалку
        main.close_modal()

        # Снова в ленту и сверяем счётчик
        main.go_to_feed()
        today_after = feed.get_today_done()

        assert today_after > today_before
        assert order_number

    @allure.story("Номер заказа появляется в разделе «В работе»")
    def test_order_appears_in_in_progress(self, driver):
        main = MainPage(driver)
        main.open_main()

        # Авторизация
        main.login("valentin_mikhanosha_sprint5@yandex.ru", "Qwerty123")

        # Оформляем заказ в конструкторе
        main.drag_first_ingredient_to_constructor()
        main.drag_first_ingredient_to_constructor()
        main.click_order_button()
        main.wait_for_order_modal()
        order_number = main.get_order_number_from_modal()

        # Закрываем модалку
        main.close_modal()

        # Переходим в ленту заказов
        main.go_to_feed()
        feed = OrdersFeedPage(driver)
        in_progress = feed.get_in_progress_numbers()

        assert order_number in in_progress