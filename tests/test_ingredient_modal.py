import allure
from pages.main_page import MainPage

@allure.feature("Модальное окно ингредиента")
class TestIngredientModal:

    @allure.story("Открытие модального окна ингредиента")
    @allure.title("Проверяем, что по клику на ингредиент открывается модальное окно с деталями")
    def test_open_ingredient_modal(self, browser):
        main_page = MainPage(browser)
        main_page.open_main_page()
        with allure.step("Кликаем по первому ингредиенту"):
            main_page.click_first_ingredient()

        with allure.step("Проверяем, что модальное окно открылось"):
            assert main_page.is_ingredient_details_open(), "Модальное окно с деталями ингредиента не открылось"

    @allure.story("Закрытие модального окна ингредиента")
    @allure.title("Проверяем, что модальное окно закрывается по клику на крестик")
    def test_close_ingredient_modal(self, browser):
        main_page = MainPage(browser)
        main_page.open_main_page()
        with allure.step("Кликаем по первому ингредиенту, чтобы открыть модальное окно"):
            main_page.click_first_ingredient()

        with allure.step("Закрываем модальное окно"):
            main_page.close_ingredient_details()

        with allure.step("Проверяем, что модальное окно закрылось"):
            assert main_page.is_ingredient_details_closed(), "Модальное окно не закрылось"
