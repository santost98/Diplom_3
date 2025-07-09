import allure
from pages.base_page import BasePage
from locators import OrderPageLocators
from selenium.webdriver.support.ui import WebDriverWait

class FeedPage(BasePage):

    @allure.step("Открываем страницу 'Лента заказов'")
    def open_feed_page(self):
        self.open("/feed")

    @allure.step("Получаем общее количество выполненных заказов")
    def get_total_orders_count(self):
        text = self.find(OrderPageLocators.ALL_ORDERS_COUNTER).text
        return int(text.replace(",", "").strip())

    @allure.step("Получаем количество заказов, выполненных сегодня")
    def get_today_orders_count(self):
        text = self.find(OrderPageLocators.TODAY_ORDERS_COUNTER).text
        return int(text.replace(",", "").strip())

    @allure.step("Проверяем наличие заказа с номером {order_id} в разделе 'В работе'")
    def is_order_in_progress(self, order_id):
        try:
            orders = self.find_all(OrderPageLocators.ORDER_LIST)
            order_id = str(order_id).strip()
            return any(order_id in order.text.strip() for order in orders if order.text.strip())
        except Exception:
            return False

    @allure.step("Ожидаем появления заказа с номером {order_id} в разделе 'В работе'")
    def wait_for_order_in_progress(self, order_id, timeout=10):
        order_id = str(order_id).strip()
        def order_appeared(driver):
            try:
                orders = self.find_all(OrderPageLocators.ORDER_LIST)
                return any(order_id in order.text.strip() for order in orders if order.text.strip())
            except Exception:
                return False
        WebDriverWait(self.driver, timeout).until(order_appeared)
