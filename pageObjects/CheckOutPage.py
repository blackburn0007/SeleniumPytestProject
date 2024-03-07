from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from utilities.BaseClass import BaseClass


class CheckOutPage(BaseClass):
    def __init__(self, driver):
        self.driver = driver

    locators = {
        'promo_code': (By.CSS_SELECTOR, '.promoCode'),
        'promo_btn': (By.CSS_SELECTOR, '.promoBtn'),
        'promo_info': (By.CSS_SELECTOR, '.promoInfo'),
        'prices': (By.XPATH, '//tr/td[5]/p'),
        'total_amount': (By.CSS_SELECTOR, '.totAmt'),
        'discount_amount': (By.CSS_SELECTOR, '.discountAmt')
    }

    def enter_promo_code(self, promo_code):
        return self.driver.find_element(*CheckOutPage.locators['promo_code']).send_keys(promo_code)

    def apply_promo_code(self):
        return self.driver.find_element(*CheckOutPage.locators['promo_btn']).click()

    def get_promo_info(self):
        # Method accepts tuple only , not expression
        self.verify_element_presence(self.driver, 10, CheckOutPage.locators['promo_info'])
        return self.driver.find_element(*CheckOutPage.locators['promo_info']).text

    def calculate(self):
        prices = self.driver.find_elements(*CheckOutPage.locators['prices'])
        total = self.driver.find_element(*CheckOutPage.locators['total_amount']).text

        summation = 0
        for price in prices:
            summation = summation + int(price.text)

        # assert total amount is equal to summation
        assert int(total) == summation

        # Calculate the discount amount
        total_after_discount = float(self.driver.find_element(*CheckOutPage.locators['discount_amount']).text)

        # assert total discount is less than total amount
        assert total_after_discount < summation

        return total_after_discount
