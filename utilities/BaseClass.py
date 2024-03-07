import inspect
import logging
import pytest
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


@pytest.mark.usefixtures('setup')
class BaseClass:
    @classmethod
    def get_logger(cls):
        logger_name = inspect.stack()[1][3]
        logger = logging.getLogger(logger_name)
        file_handler = logging.FileHandler("logger.log")
        formatter = logging.Formatter("%(asctime)s :%(levelname)s : %(name)s : %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.setLevel(logging.INFO)
        return logger

    def verify_element_presence(self, driver, timeout, element):
        try:
            WebDriverWait(driver, timeout).until(
                expected_conditions.presence_of_element_located(element))
        except TimeoutException:
            self.get_logger().error(f"Element {element} is not present")
            assert False

