import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from urls import BASE_URL

class BasePage:
    def __init__(self, driver, base_url=BASE_URL):
        self.driver = driver
        self.base_url = base_url

    @allure.step("Открываем страницу: {url}")
    def open(self, url=""):
        self.driver.get(self.base_url + url)

    @allure.step("Ищем элемент на странице: {locator}")
    def find(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    @allure.step("Ожидаем видимость элемента: {locator}")
    def wait_for_visibility(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    @allure.step("Ожидаем, что элемент станет невидимым: {locator}")
    def wait_for_invisibility(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )

    @allure.step("Ожидаем, что элемент станет кликабельным: {locator}")
    def wait_for_clickable(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    @allure.step("Ожидаем, пока элемент станет кликабельным: {locator}")
    def find_clickable(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    @allure.step("Ищем все элементы: {locator}")
    def find_all(self, locator, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(locator)
        )
        return self.driver.find_elements(*locator)

    @allure.step("Кликаем по элементу: {locator}")
    def click(self, locator, timeout=10):
        self.find_clickable(locator, timeout).click()

    @allure.step("Кликаем по элементу с помощью JavaScript: {locator}")
    def js_click(self, locator):
        element = self.find(locator)
        self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Проверяем, отображается ли элемент: {locator}")
    def is_displayed(self, locator, timeout=10):
        try:
            return self.find(locator, timeout).is_displayed()
        except TimeoutException:
            return False

    @allure.step("Проверяем, что элемент не отображается: {locator}")
    def is_not_displayed(self, locator, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    @allure.step("Проверяем, что в URL содержится подстрока: {substring}")
    def current_url_contains(self, substring: str, timeout=10) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(lambda d: substring in d.current_url)
            return True
        except TimeoutException:
            return False

    @allure.step("Получаем текущий URL")
    def get_current_url(self):
        return self.driver.current_url

    @allure.step("Ожидаем, что текст элемента {locator} изменится с '{old_text}'")
    def wait_for_text_change(self, locator, old_text, timeout=10):
        def text_changed(driver):
            try:
                element = driver.find_element(*locator)
                return element.text.strip() != str(old_text)
            except Exception:
                return False
        WebDriverWait(self.driver, timeout).until(text_changed)
