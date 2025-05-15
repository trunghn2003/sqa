import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestSearchBook(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chromedriver_path = r"D:\Ky 2 nam 4\SQA\sqa\chromedriver.exe"
        service = Service(executable_path=chromedriver_path)
        cls.driver = webdriver.Chrome(service=service)
        cls.base_url = "http://localhost:8000"

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def login(self):
        driver = self.driver
        driver.get(f"{self.base_url}/login/")
        driver.find_element(By.ID, "email").send_keys("phamhuyhoa03@gmail.com")
        driver.find_element(By.ID, "password").send_keys("huyhoa10102003")
        driver.find_element(By.ID, "login").click()
        WebDriverWait(driver, 10).until(lambda d: "/login" not in d.current_url)

    def test_search_book(self):
        self.login()
        driver = self.driver
        driver.get(f"{self.base_url}/books/?search=Test")
        results = driver.find_elements(By.CSS_SELECTOR, ".book-item")
        self.assertTrue(any("Test" in r.text for r in results))

if __name__ == '__main__':
    unittest.main()
