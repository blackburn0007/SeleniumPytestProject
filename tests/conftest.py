import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService, Service
from selenium.webdriver.firefox.service import Service as FirefoxService

from TestData.HomePageData import HomePageData

driver = None


# Command line options
def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome",
        help="Choose the browser to use (chrome, firefox, ie). Default is chrome."
    )
    parser.addoption(
        "--url", action="store", default="test",
        help="Choose the URL to connect to"
    )


# Request is a default instance of a fixture

@pytest.fixture(scope="class")
def setup(request):
    browser_name = request.config.getoption("browser_name")
    global driver
    if browser_name == "chrome":
        options = ChromeOptions()
        service = Service()
        driver = webdriver.Chrome(service=service, options=options)
    elif browser_name == "firefox":
        options = FirefoxOptions()
        options.binary_location = "/usr/bin/firefox"
        service = FirefoxService("/home/siyavush/Downloads/WebDrivers/geckodriver")
        driver = webdriver.Firefox(options=options, service=service)
    elif browser_name == "ie":
        print('IE browser is executed')
    else:
        raise ValueError("Invalid browser name")

    driver.maximize_window()
    url = request.config.getoption("url")
    if url == "test":
        driver.get('https://rahulshettyacademy.com/seleniumPractise/#/')
    print(driver.current_url)
    request.cls.driver = driver
    yield
    driver.close()


# Parameterizing WebDriver tests with multiple datasets (optional)
# We can also get Excel data here
@pytest.fixture(params=[HomePageData.test_HomePageData])
def getData(request):
    return request.param


# Automatic screenshot capture on test failures
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
        Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
        :param item:
        """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extras', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'was_xfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            _capture_screenshot(file_name)
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append(pytest_html.extras.html(html))
        report.extras = extra


def _capture_screenshot(name):
    driver.get_screenshot_as_file(name)
