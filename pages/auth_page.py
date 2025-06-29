import allure
from pages.base_page import BasePage
from locators import AccountPageLocators

class AuthPage(BasePage):

    @allure.step("Вводим email: {email}")
    def enter_email(self, email):
        email_input = self.find(AccountPageLocators.INPUT_EMAIL)
        email_input.clear()
        email_input.send_keys(email)

    @allure.step("Вводим пароль")
    def enter_password(self, password):
        password_input = self.find(AccountPageLocators.INPUT_PASSWORD)
        password_input.clear()
        password_input.send_keys(password)

    @allure.step("Нажимаем кнопку Войти")
    def click_login_button(self):
        self.click(AccountPageLocators.BUTTON_ENTER)

    @allure.step("Логинимся с email: {email}")
    def login(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()
