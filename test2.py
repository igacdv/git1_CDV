import unittest
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

first_name = "Marcin"
last_name = "Nowak"
gender = "male"
country_code = "+48"
telephone = "123123123"
invalid_email = "jhjfdj.pl"
password = "Fjhg65476ghd"
chosen_country = "Polska"

class WizzairRegistration(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://wizzair.com/pl-pl/#/")
        self.driver.maximize_window()
        self.driver.implicitly_wait(50)

    def tearDown(self):
        self.driver.quit()

    def test_invalid_email(self):
        driver = self.driver
        zaloguj_btn = driver.find_element_by_css_selector('button[data-test="navigation-menu-signin"]')
        zaloguj_btn.click()
        rejestracja_btn = driver.find_element_by_xpath('//button[@data-test="registration"]')
        rejestracja_btn.click()
        first_name_input = driver.find_element_by_name("firstName")
        first_name_input.send_keys(first_name)
        driver.find_element_by_name("lastName").send_keys(last_name)
        if gender == "female":
            driver.find_element_by_xpath('//label[@data-test="register-genderfemale"]').click()
        else:
            first_name_input.click()
            driver.find_element_by_xpath('//label[@data-test="register-gendermale"]').click()

        # 6. Wpisz kod kraju
        # Wyszukanie diva z kodem kraju
        driver.find_element_by_xpath('//div[@data-test="booking-register-country-code"]').click()
        # Wyszukanie inputa do wpisania kodu
        country_code_input = driver.find_element_by_name('phone-number-country-code')
        # Kliknięcie w inputa
        country_code_input.click()
        # Wpisanie kodu kraju i potwierdzenie ENTEREM
        country_code_input.send_keys(country_code + Keys.RETURN)
        # 7. Wpisz numer telefonu
        driver.find_element_by_name("phoneNumberValidDigits").send_keys(telephone)
        # 8. Wpisz niepoprawny e-mail (brak znaku "@')
        driver.find_element_by_name("email").send_keys(invalid_email)
        # 9. Wpisz hasło
        driver.find_element_by_xpath('//input[@data-test="booking-register-password"]').send_keys(password)
        # 10. Wybierz narodowość
        # Kliknięcie w input, żeby rozwinąć kraje
        driver.find_element_by_xpath('//input[@data-test="booking-register-country"]').click()
        # Wyszukanie konteneru z krajami
        countries_container = driver.find_element_by_class_name('register-form__country-container__locations')
        # Szukam WEWNĄTRZ konteneru z krajami labelek
        # Metoda zwróci LISTĘ WebElementów [WebElement, WebElement, Webelement....]
        countries_list = countries_container.find_elements_by_tag_name('label')
        print("Liczba krajów", len(countries_list))
        # Powtarzaj dla każdego elementu w liście krajów
        for label in countries_list:
            # Szukaj wewnątrz elementu label
            country = label.find_element_by_tag_name('strong')
            # Pobierz i wypisz wewnętrzny tekst elementu country
            # print(country.get_attribute("innerText"))
            # Jeśli to szukany kraj
            if country.get_attribute("innerText") == chosen_country:
                # Przewiń do wybranego kraju
                country.location_once_scrolled_into_view
                # To w niego kliknij
                country.click()
                #... i nie szukaj dalej
                break

        error_notices = driver.find_elements_by_xpath('//span[@class="input-error__message"]/span')
        visible_error_notices = []
        for error in error_notices:
            if error.is_displayed():
                visible_error_notices.append(error)

        assert len(visible_error_notices) == 1
        assert visible_error_notices[0].text == "Nieprawidłowy adres e-mail"
        self.assertEqual(visible_error_notices[0].text, "Nieprawidłowy adres e-mail")
        sleep(3)

    def test_invalid_phone_number(self):
        pass

if __name__ == "__main__":
    unittest.main(verbosity=2)