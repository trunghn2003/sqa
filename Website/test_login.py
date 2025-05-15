import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException  

class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chromedriver_path = r"D:\Ky 2 nam 4\SQA\sqa\chromedriver.exe"
        service = Service(executable_path=chromedriver_path)
        cls.driver = webdriver.Chrome(service=service)
        cls.base_url = "http://localhost:8000"

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_login(self):
        print("[TestLogin] Bắt đầu test đăng nhập")
        try:
            driver = self.driver
            print("[TestLogin] Mở trang login")
            driver.get(f"{self.base_url}/login")
            print("[TestLogin] Nhập email và mật khẩu")
            driver.find_element(By.ID, "email").send_keys("phamhuyhoa03@gmail.com")
            driver.find_element(By.ID, "password").send_keys("huyhoa10102003")
            print("[TestLogin] Nhấn nút đăng nhập")
            driver.find_element(By.ID, "login").click()
            WebDriverWait(driver, 10).until(lambda d: "/login" not in d.current_url)
            print("[TestLogin] PASS: Đăng nhập thành công, chuyển hướng khỏi /login")
            self.assertNotIn("/login", driver.current_url)
        except TimeoutException as e:
            print(f"[TestLogin] FAIL: Quá thời gian chờ đăng nhập: {e}")
            self.fail("Timeout waiting during login test")

if __name__ == '__main__':
    unittest.main()
