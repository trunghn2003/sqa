import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestRateBook(unittest.TestCase):
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

    def test_rate_book(self):
        self.login()
        driver = self.driver
        driver.get(f"{self.base_url}/books/1/")
        star = driver.find_element(By.CSS_SELECTOR, ".star-rating input[value='5']")
        star.click()
        driver.find_element(By.CSS_SELECTOR, "button.submit-rating").click()
        rating = driver.find_element(By.CLASS_NAME, "current-rating")
        self.assertIn("5", rating.text)

if __name__ == '__main__':
    unittest.main()
