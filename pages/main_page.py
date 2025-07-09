import allure
from pages.base_page import BasePage
from locators import MainPageLocators
from seletools.actions import drag_and_drop
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class MainPage(BasePage):

    @allure.step("Открываем главную страницу")
    def open_main_page(self):
        self.open()

    @allure.step("Переходим в раздел 'Конструктор'")
    def click_constructor(self):
        self.click(MainPageLocators.CONSTRUCTOR_BUTTON)

    @allure.step("Переходим в раздел 'Лента заказов'")
    def click_orders_feed(self):
        self.click(MainPageLocators.ORDERS_FEED_BUTTON)

    @allure.step("Кликаем по первому ингредиенту (булке)")
    def click_first_ingredient(self):
        self.js_click(MainPageLocators.BUN_INGREDIENT)

    @allure.step("Проверяем, что окно деталей ингредиента отображается")
    def is_ingredient_details_open(self):
        return self.is_displayed(MainPageLocators.INGREDIENT_DETAILS)

    @allure.step("Закрываем окно деталей ингредиента")
    def close_ingredient_details(self):
        # 1. Ждём исчезновения оверлея (если он есть)
        overlay_locator = (By.CSS_SELECTOR, "div[class*='modal_overlay']")
        try:
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located(overlay_locator)
            )
        except Exception:
            pass  # Если оверлея нет — продолжаем
        # 2. Ждём кликабельности кнопки
        close_btn_locator = MainPageLocators.CLOSE_POP_UP_INGREDIENT_DETAILS_BUTTON
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(close_btn_locator)
        )
        # 3. Обычный клик
        self.click(close_btn_locator)
        assert self.is_ingredient_details_closed(), "Модальное окно не закрылось после клика по крестику"

    def is_ingredient_details_closed(self):
        return self.is_not_displayed(MainPageLocators.INGREDIENT_DETAILS)

    @allure.step("Получаем счётчик ингредиента (булка)")
    def get_bun_ingredient_counter(self):
        text = self.find(MainPageLocators.COUNTER).text
        try:
            return int(text)
        except ValueError:
            return 0

    @allure.step("Добавляем булку в заказ (перетаскиваем булку в конструктор и закрываем модальное окно)")
    def add_bun_ingredient_to_order(self):
        source = self.find(MainPageLocators.BUN_INGREDIENT)
        target = self.find(MainPageLocators.CONSTRUCTOR_FIELD)
        drag_and_drop(self.driver, source, target)
        # Если после dnd появляется модалка с деталями, закрываем её
        if self.is_displayed(MainPageLocators.INGREDIENT_DETAILS, timeout=2):
            self.close_ingredient_details()

    @allure.step("Получаем номер созданного заказа")
    def get_order_id(self):
        return self.find(MainPageLocators.ORDER_ID).text.strip()
