import allure
from locators import MainPageLocators, OrderPageLocators
from pages.main_page import MainPage
from pages.feed_page import FeedPage
import time
from selenium.webdriver.common.by import By

@allure.feature("Проверка функционала заказа в Stellar Burgers")
class TestOrderFlow:

    @allure.story("Проверка открытия модального окна ингредиента и его закрытия")
    @allure.title("Открываем и закрываем окно деталей ингредиента")
    def test_ingredient_modal_open_and_close(self, authorized_browser):
        main_page = MainPage(authorized_browser)
        main_page.open_main_page()
        with allure.step("Кликаем по первому ингредиенту (булке)"):
            main_page.click_first_ingredient()
        with allure.step("Проверяем, что модальное окно открылось"):
            assert main_page.is_ingredient_details_open(), "Модальное окно не открылось"
        with allure.step("Закрываем модальное окно"):
            main_page.close_ingredient_details()
        with allure.step("Проверяем, что модальное окно закрылось"):
            assert main_page.is_ingredient_details_closed(), "Модальное окно не закрылось"

    @allure.story("Проверка увеличения счётчика ингредиента")
    @allure.title("Добавляем ингредиент и проверяем счётчик")
    def test_ingredient_counter_increases(self, authorized_browser):
        main_page = MainPage(authorized_browser)
        main_page.open_main_page()
        initial_counter = main_page.get_bun_ingredient_counter()
        with allure.step("Добавляем булку в заказ"):
            main_page.add_bun_ingredient_to_order()
        with allure.step("Проверяем, что счётчик увеличился"):
            new_counter = main_page.get_bun_ingredient_counter()
            assert new_counter > initial_counter, "Счётчик ингредиента не увеличился"

    @allure.story("Проверка увеличения счётчиков заказов после создания нового заказа")
    @allure.title("Создаём заказ и проверяем счётчики 'Выполнено за всё время' и 'Выполнено за сегодня'")
    def test_order_counters_increment_after_order(self, authorized_browser):
        main_page = MainPage(authorized_browser)
        feed_page = FeedPage(authorized_browser)

        # 1. Дождаться загрузки конструктора
        main_page.wait_for_visibility(MainPageLocators.CREATE_BURGER_TEXT)

        # 2. Перейти в ленту заказов и запомнить счётчики
        feed_page.open_feed_page()
        feed_page.wait_for_visibility(OrderPageLocators.ALL_ORDERS_COUNTER)
        total_before = feed_page.get_total_orders_count()
        today_before = feed_page.get_today_orders_count()

        # 3. Вернуться в конструктор
        main_page.open_main_page()
        main_page.wait_for_visibility(MainPageLocators.CONSTRUCTOR_FIELD)

        with allure.step("Добавляем булку в заказ и оформляем заказ"):
            main_page.add_bun_ingredient_to_order()
            main_page.wait_for_clickable(MainPageLocators.ORDER_BUTTON)
            main_page.click(MainPageLocators.ORDER_BUTTON)

        with allure.step("Получаем номер созданного заказа"):
            main_page.wait_for_visibility(MainPageLocators.ORDER_ID)
            order_id = main_page.get_order_id()
            assert order_id, "Не удалось получить номер заказа — он пустой или None"

            main_page.wait_for_visibility(MainPageLocators.ORDER_POP_UP)
            # Закрыть окно заказа через универсальный селектор
            close_button = (By.CSS_SELECTOR, "button[class*='modal__close']")
            main_page.js_click(close_button)
            main_page.wait_for_invisibility(MainPageLocators.ORDER_POP_UP)

        # 4. Перейти в ленту заказов
        feed_page.open_feed_page()
        feed_page.wait_for_visibility(OrderPageLocators.ALL_ORDERS_COUNTER)

        #  Ждём, пока значения счётчиков увеличатся
        feed_page.wait_for_text_change(OrderPageLocators.ALL_ORDERS_COUNTER, total_before)
        feed_page.wait_for_text_change(OrderPageLocators.TODAY_ORDERS_COUNTER, today_before)

        total_after = feed_page.get_total_orders_count()
        today_after = feed_page.get_today_orders_count()

        with allure.step("Проверяем, что общее количество заказов увеличилось"):
            assert total_after > total_before, f"Общее количество заказов не увеличилось: было {total_before}, стало {total_after}"

        with allure.step("Проверяем, что количество заказов за сегодня увеличилось"):
            assert today_after > today_before, f"Заказов за сегодня не увеличилось: было {today_before}, стало {today_after}"

        with allure.step(f"Проверяем, что заказ с номером {order_id} отображается в разделе 'В работе'"):
            feed_page.wait_for_order_in_progress(order_id)
