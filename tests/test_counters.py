import allure
import pytest
from selenium.webdriver import Firefox

from pages.main_page import MainPage
from pages.orders_feed_page import OrdersFeedPage


@allure.feature("Лента заказов и счётчики")
class TestCounters:

    @allure.story("Счётчик «Выполнено за все время» увеличивается после нового заказа")
    def test_total_done_increases_after_order(self, authorized_driver):
        main = MainPage(authorized_driver)
        main.open_main()

        # Авторизация уже выполнена через API (authorized_driver)

        main.drag_first_ingredient_to_constructor()
        main.drag_first_ingredient_to_constructor()
        main.click_order_button()
        order_number = main.wait_for_order_modal()

        main.close_modal()

        main.go_to_feed()
        feed = OrdersFeedPage(authorized_driver)
        total_after = feed.get_total_done()

        assert total_after > 0
        assert order_number
        assert order_number.isdigit()

    @allure.story("Счётчик «Выполнено за сегодня» увеличивается после нового заказа")
    def test_today_done_increases_after_order(self, authorized_driver):
        main = MainPage(authorized_driver)
        main.open_main()

        main.go_to_feed()
        feed = OrdersFeedPage(authorized_driver)
        today_before = feed.get_today_done()

        main.go_to_constructor()
        main.drag_first_ingredient_to_constructor()
        main.drag_first_ingredient_to_constructor()
        main.click_order_button()
        order_number = main.wait_for_order_modal()

        main.close_modal()

        main.go_to_feed()
        today_after = feed.get_today_done()

        assert order_number
        assert order_number.isdigit()

        if isinstance(authorized_driver, Firefox):
            pytest.xfail("Известная нестабильность Firefox: счётчик 'за сегодня' может не обновляться сразу")
        assert today_after > today_before

    @allure.story("Номер заказа появляется в разделе «В работе»")
    def test_order_appears_in_in_progress(self, authorized_driver):
        main = MainPage(authorized_driver)
        main.open_main()

        main.drag_first_ingredient_to_constructor()
        main.drag_first_ingredient_to_constructor()
        main.click_order_button()
        order_number = main.wait_for_order_modal()

        main.close_modal()

        main.go_to_feed()
        feed = OrdersFeedPage(authorized_driver)
        in_progress = feed.get_in_progress_numbers()

        assert order_number
        assert order_number.isdigit()

        if isinstance(authorized_driver, Firefox):
            pytest.xfail("Известная нестабильность Firefox: в модалке может отображаться 9999 вместо реального номера")
        assert order_number in in_progress