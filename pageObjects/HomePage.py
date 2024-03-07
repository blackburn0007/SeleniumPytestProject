from selenium.webdriver.common.by import By
from pageObjects.CheckOutPage import CheckOutPage
from utilities.BaseClass import BaseClass


class HomePage(BaseClass):
    # Class instance to create driver object
    def __init__(self, driver):
        self.driver = driver

    locators = {
        'search_btn': (By.CSS_SELECTOR, 'input[type="search"]'),
        'results': (By.XPATH, '//div[@class="products"]/div'),
        'product_names': (By.XPATH, 'h4'),
        'add_to_cart_btn': (By.XPATH, 'div/button'),
        'cart_icon': (By.CSS_SELECTOR, '.cart-icon'),
        'proceed_to_checkout': (By.XPATH, '//button[contains(text(), "PROCEED TO CHECKOUT")]')
    }

    def search_items(self, search_word):
        # star before Class name treats locator as a tuple which is what we need
        return self.driver.find_element(*HomePage.locators['search_btn']).send_keys(search_word)

    def get_products(self):
        # A list to store the products
        products_list = []
        results = self.driver.find_elements(*HomePage.locators['results'])
        assert len(results) > 0
        # Loop through the elements that contain product information
        for product in results:
            # Click on the button to add the product to the cart
            product.find_element(*HomePage.locators['add_to_cart_btn']).click()
            # Get the product name from the h4 element
            product_name = product.find_element(*HomePage.locators['product_names']).text
            # Append the product name to the list
            products_list.append(product_name)
        # Return the list of products
        return products_list

    def add_to_cart(self):
        return self.driver.find_element(*HomePage.locators['cart_icon']).click()

    def move_to_checkout(self):
        self.driver.find_element(*HomePage.locators['proceed_to_checkout']).click()
        # By importing checkout class here we eliminate need for constant driver assigning
        checkout_page = CheckOutPage(self.driver)
        return checkout_page
