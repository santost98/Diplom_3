import allure
from locators import MainPageLocators, OrderPageLocators
from pages.main_page import MainPage
from pages.feed_page import FeedPage

@allure.feature("Навигация по сайту")
class TestNavigation:

    @allure.story("Переход по кнопке Конструктор")
    @allure.title("Проверяем, что при клике на 'Конструктор' открывается главная страница конструктора")
    def test_click_constructor(self, browser):
        main_page = MainPage(browser)
        main_page.open_main_page()
        with allure.step("Кликаем на кнопку 'Конструктор'"):
            main_page.click_constructor()

        with allure.step("Проверяем, что отображается текст 'Соберите бургер'"):
            assert main_page.is_displayed(MainPageLocators.CREATE_BURGER_TEXT), "Страница конструктора не открылась"

    @allure.story("Переход по кнопке Лента заказов")
    @allure.title("Проверяем, что при клике на 'Лента заказов' открывается страница с лентой заказов")
    def test_click_orders_feed(self, browser):
        main_page = MainPage(browser)
        feed_page = FeedPage(browser)
        main_page.open_main_page()
        with allure.step("Кликаем на кнопку 'Лента заказов'"):
            main_page.click_orders_feed()

        with allure.step("Проверяем, что произошёл переход на /feed"):
            assert "/feed" in feed_page.get_current_url(), "URL не содержит /feed"

        with allure.step("Проверяем, что отображается счётчик заказов"):
            assert feed_page.is_displayed(OrderPageLocators.ALL_ORDERS_COUNTER), \
                "Счётчик заказов не отображается — страница ленты заказов не загрузилась"
