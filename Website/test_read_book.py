import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time

class TestReadBook(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("[TestReadBook] Khởi động trình duyệt Chrome và mở URL cơ sở")
        chromedriver_path = r"D:\Ky 2 nam 4\SQA\sqa\chromedriver.exe"
        service = Service(executable_path=chromedriver_path)
        cls.driver = webdriver.Chrome(service=service)
        cls.base_url = "http://localhost:8000"

    @classmethod
    def tearDownClass(cls):
        print("[TestReadBook] Đóng trình duyệt Chrome")
        cls.driver.quit()

    def login(self):
        print("[TestReadBook] Bắt đầu đăng nhập...")
        driver = self.driver
        driver.get(f"{self.base_url}/login")
        driver.find_element(By.ID, "email").send_keys("phamhuyhoa03@gmail.com")
        driver.find_element(By.ID, "password").send_keys("huyhoa10102003")
        driver.find_element(By.ID, "login").click()
        WebDriverWait(driver, 10).until(lambda d: "/login" not in d.current_url)
        print("[TestReadBook] Đã đăng nhập thành công")

    def test_read_book_feature(self):
        try:
            print("[TestReadBook] Bắt đầu test chức năng đọc sách")
            self.login()
            driver = self.driver
            driver.get(f"{self.base_url}/viewBookPage/11")
            driver.find_element(By.ID, "open_book").click()
            WebDriverWait(driver, 10).until(lambda d: "/OpenBookPage/11" in d.current_url)
            print("[TestReadBook] Đã chuyển hướng thành công tới OpenBookPage")
            self.assertIn("/OpenBookPage/11", driver.current_url)
            print("[TestReadBook] PASS: Read Book feature test")
        except TimeoutException as e:
            print(f"[TestReadBook] FAIL: Read Book feature test timeout: {e}")
            self.fail("Timeout waiting for page navigation in test_read_book_feature")

    def test_translate_feature(self):
        try:
            print("[TestReadBook] Bắt đầu test tính năng dịch sách")
            self.login()
            driver = self.driver
            driver.get(f"{self.base_url}/viewBookPage/11")
            driver.find_element(By.ID, "open_book").click()
            WebDriverWait(driver, 10).until(lambda d: "/OpenBookPage/11" in d.current_url)
            print("[TestReadBook] Đã mở trang đọc sách và chuyển hướng thành công tới OpenBookPage")
            driver.find_element(By.ID, "tools_image").click()
            WebDriverWait(driver, 10).until(lambda d: d.find_element(By.ID, "translate-text").is_displayed())
            textarea = driver.find_element(By.ID, "translate-text")
            original_text = "This is a test for translation."
            textarea.send_keys(original_text)
            print(f"[TestReadBook] Đã nhập văn bản gốc: {original_text}")
            driver.find_element(By.CSS_SELECTOR, "button[onclick*='translate']").click()
            print("[TestReadBook] Đã bấm Start Translation")
            WebDriverWait(driver, 10).until(lambda d: d.find_element(By.ID, "translate-text").get_attribute("value") != original_text)
            translated_text = driver.find_element(By.ID, "translate-text").get_attribute("value")
            print(f"[TestReadBook] Kết quả dịch: {translated_text}")
            self.assertNotEqual(original_text, translated_text)
            print("[TestReadBook] PASS: Translate feature test")
        except TimeoutException as e:
            print(f"[TestReadBook] FAIL: Translate feature test timeout: {e}")
            self.fail("Timeout waiting during translation feature test")

    def test_note_feature(self):
        try:
            print("[TestReadBook] Bắt đầu test tính năng Note")
            self.login()
            driver = self.driver
            driver.get(f"{self.base_url}/viewBookPage/11")
            driver.find_element(By.ID, "open_book").click()
            WebDriverWait(driver, 10).until(lambda d: "/OpenBookPage/11" in d.current_url)
            driver.find_element(By.ID, "tools_image").click()
            # Đợi textarea của Notes hiển thị using XPath locator
            note_area = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//h3[text()='Notes']/following-sibling::textarea"))
            )
            note_text = "This is a test note."
            note_area.send_keys(note_text)
            note_area.send_keys(Keys.ENTER)
            print(f"[TestReadBook] Đã nhập và gửi note: {note_text}")
            # Chờ textarea Notes được làm mới (trống)
            WebDriverWait(driver, 5).until(
                lambda d: d.find_element(By.XPATH, "//h3[text()='Notes']/following-sibling::textarea").get_attribute("value") == ""
            )
            self.assertEqual("", driver.find_element(By.XPATH, "//h3[text()='Notes']/following-sibling::textarea").get_attribute("value"))
            print("[TestReadBook] PASS: Note feature test")
        except TimeoutException as e:
            print(f"[TestReadBook] FAIL: Note feature test timeout: {e}")
            self.fail("Timeout waiting during note feature test")

    def test_tts_feature(self):
        try:
            print("[TestReadBook] Bắt đầu test tính năng Text-to-Speech")
            self.login()
            driver = self.driver
            driver.get(f"{self.base_url}/viewBookPage/11")
            driver.find_element(By.ID, "open_book").click()
            WebDriverWait(driver, 10).until(lambda d: "/OpenBookPage/11" in d.current_url)
            driver.find_element(By.ID, "tools_image").click()
            WebDriverWait(driver, 10).until(lambda d: d.find_element(By.ID, "tts-text").is_displayed())
            tts_area = driver.find_element(By.ID, "tts-text")
            en_text = "Hello world"
            tts_area.send_keys(en_text)
            driver.find_element(By.ID, "play").click()
            print(f"[TestReadBook] Đã bấm Start Text to Speech với văn bản: {en_text}")
            time.sleep(3)
            driver.find_element(By.ID, "stop").click()
            print("[TestReadBook] Đã bấm Stop Speech")
            print("[TestReadBook] PASS: Text-to-Speech feature test")
        except TimeoutException as e:
            print(f"[TestReadBook] FAIL: TTS feature test timeout: {e}")
            self.fail("Timeout waiting during TTS feature test")

    def test_summarize_feature(self):
        try:
            print("[TestReadBook] Bắt đầu test tính năng Summarization")
            self.login()
            driver = self.driver
            driver.get(f"{self.base_url}/viewBookPage/11")
            driver.find_element(By.ID, "open_book").click()
            WebDriverWait(driver, 10).until(lambda d: "/OpenBookPage/11" in d.current_url)
            driver.find_element(By.ID, "tools_image").click()
            WebDriverWait(driver, 10).until(lambda d: d.find_element(By.ID, "summarize-text").is_displayed())
            sum_area = driver.find_element(By.ID, "summarize-text")
            original_para = "This is a long paragraph for summarization test. It should be shortened."
            sum_area.send_keys(original_para)
            driver.find_element(By.CSS_SELECTOR, "button[onclick*='summarize']").click()
            WebDriverWait(driver, 10).until(lambda d: d.find_element(By.ID, "summarize-text").get_attribute("value") != original_para)
            summary = driver.find_element(By.ID, "summarize-text").get_attribute("value")
            print(f"[TestReadBook] Kết quả tóm tắt: {summary}")
            self.assertNotEqual(original_para, summary)
            print("[TestReadBook] PASS: Summarization feature test")
        except TimeoutException as e:
            print(f"[TestReadBook] FAIL: Summarization feature test timeout: {e}")
            self.fail("Timeout waiting during summarization feature test")

if __name__ == '__main__':
    unittest.main()
