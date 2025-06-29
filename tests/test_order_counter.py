import allure
from pages.feed_page import FeedPage

@allure.feature("Счётчики заказов")
class TestOrderCounter:

    @allure.story("Проверка счётчиков заказов")
    @allure.title("Проверяем, что счётчики 'Выполнено за всё время' и 'Выполнено за сегодня' отображаются")
    def test_order_counters_visibility(self, browser):
        feed_page = FeedPage(browser)
        feed_page.open_feed_page()
        counters = {
            "Общее количество заказов": feed_page.get_total_orders_count(),
            "Количество заказов за сегодня": feed_page.get_today_orders_count()
        }
        for name, value in counters.items():
            assert value is not None and value >= 0, f"{name} отсутствует или меньше 0"
