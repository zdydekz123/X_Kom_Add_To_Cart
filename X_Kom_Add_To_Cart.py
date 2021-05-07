from selenium import webdriver
import unittest
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


search_value = "laptop"


class XkomAddToCart(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        # 1. Wejdź na stronę "https://www.x-kom.pl/".
        self.driver.get("https://www.x-kom.pl/")
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()

    def testCheckTotalValueProducts(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        # 2. Kliknij w puste pole głównej wyszukiwarki sklepu
        search_field = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Czego szukasz?"]')))
        search_field.click()
        placeholder = search_field.get_attribute('placeholder')
        assert placeholder == 'Czego szukasz?'
        print('Potwierdzenie nazwy pola wyszukiwania: ' + placeholder)

        # 3. W polu wyszukiwarki wpisz wartość "laptop"
        search_field.send_keys(search_value)

        # 4. Wyszukaj pozadana wartosc naciskajac w submit button
        search_submit = driver.find_element_by_css_selector("button.apKoa")
        search_submit.click()

        # Sprawdzamy czy istnieja produkty w sklepie o pozadanej wartosci
        try:
            no_search_results = driver.find_element_by_class_name('jWLcUU').get_attribute('textContent')
            result_complement = driver.find_element_by_class_name('ceCpjl').get_attribute('textContent')
            assert 'Brak wyników dla ' + result_complement + '.' not in no_search_results
            print(no_search_results)
        except NoSuchElementException:
            amount_search_results = driver.find_element_by_class_name('gfzxIs').get_attribute('textContent')
            print('Ilość produktów: ' + amount_search_results)


        #  5. Kolejno z listy produktów, wybierz element z dostępnym przyciskiem "Dodaj do koszyka”.
        button_enabled = driver.find_elements_by_xpath("//button[@title='Dodaj do koszyka' and not(@disabled)]")
        button_enabled[0].click()

        # 6. Po wyświetleniu okna popup kliknij w przycisk "Przejdź do koszyka".
        order_popup = driver.find_element_by_class_name('modal')
        button_gtb = driver.find_element_by_partial_link_text("Przejdź do koszyka")
        if order_popup.is_displayed():
            button_gtb.click()
            print('Okno kontynuacji zamówienia jest dostępne')
        else:
            print('Okno kontynuacji zamówienia jest niedostępne')
            driver.close()

        # (VERIFICATION) Czy produkt został poprawnie dodany do koszyka
        basket_value = driver.find_element_by_class_name("bokHoB")
        go_to_delivery = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'jSCQpQ')))
        # Jeśli wartość obok nazwy "Koszyk" jest równa 1 to kliknij w button "Przejdź do dostawy"
        if basket_value.text[-1] != "0":
            assert basket_value.text[-1] >= '1'
            go_to_delivery.click()
            print("Produkt został poprawnie dodany do koszyka!")
            print("Łączna ilość produktów w koszyku to: " + basket_value.text[-1])
        else:
            assert basket_value.text[-1] <= '0'
            print("Produkt nie został poprawnie dodany do koszyka!")
            print("Łączna ilość produktów w koszyku to: " + basket_value.text[-1])
            driver.close()

        sleep(5)


if __name__ == "__main__":
    unittest.main(verbosity=2)