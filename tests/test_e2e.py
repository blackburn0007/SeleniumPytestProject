from selenium.webdriver.common.by import By
import time
from pageObjects.HomePage import HomePage
from pageObjects.CheckOutPage import CheckOutPage
from utilities.BaseClass import BaseClass


class TestOne(BaseClass):

    def test_e2e(self):
        # Using page object model
        homepage = HomePage(self.driver)

        log = self.get_logger()

        # global wait
        self.driver.implicitly_wait(2)

        # search and wait
        homepage.search_items('berry')
        time.sleep(2)
        log.info('search is successful')

        #assert tbat right products were chosen
        expected_list = ['Cucumber - 1 Kg', 'Raspberry - 1/4 Kg', 'Strawberry - 1/4 Kg']
        assert homepage.get_products() == expected_list
        log.info('products are present')

        # add to the cart
        homepage.add_to_cart()
        log.info("products are added to cart")

        # prcoeed to checkout
        check_out_page = homepage.move_to_checkout()
        log.info('proceeded to checkout')

        # enter promo code
        check_out_page.enter_promo_code('rahulshettyacademy')
        log.info('promo code entered')
        # apply promo code
        check_out_page.apply_promo_code()
        log.info('promo code applied')

        # assert promo code applied
        assert check_out_page.get_promo_info() == 'Code applied ..!'
        log.info("promod code is correct")

        # assert total amount is correct
        check_out_page.calculate()
        log.info('You need to pay %s amount', check_out_page.calculate())


