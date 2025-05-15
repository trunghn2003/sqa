import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import os
import random
import time

class TestUploadBook(unittest.TestCase):
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
        print("TestUploadBook: Bắt đầu đăng nhập...")
        driver = self.driver
        driver.get(f"{self.base_url}/login")
        driver.find_element(By.ID, "email").send_keys("phamhuyhoa03@gmail.com")
        driver.find_element(By.ID, "password").send_keys("huyhoa10102003")
        driver.find_element(By.ID, "login").click()
        WebDriverWait(driver, 10).until(lambda d: "/login" not in d.current_url)
        print("TestUploadBook: Đăng nhập thành công")

    def test_upload_book(self):
        try:
            print("TestUploadBook: Bắt đầu test upload sách qua UI")
            self.login()
            driver = self.driver
            user_icon = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "user"))
            )
            ActionChains(driver).move_to_element(user_icon).perform()
            time.sleep(1)
            dropdown_items = driver.find_elements(By.XPATH, "//li")
            found = False
            for item in dropdown_items:
                if "my uploaded book" in item.text.strip().lower():
                    item.click()
                    found = True
                    break
            for _ in range(20):
                current_url = driver.current_url
                if "/myUploadedBookPage" in current_url:
                    break
                time.sleep(0.5)
            else:
                print("TestUploadBook FAIL: Không chuyển sang giao diện My Uploaded Book sau khi click menu!")
                self.fail("Không chuyển sang giao diện My Uploaded Book!")
            upload_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "upload_book"))
            )
            upload_btn.click()
            print("TestUploadBook: Mở modal Upload Book")
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "upload-book-container"))
            )
            title_input = driver.find_element(By.ID, "title")
            author_input = driver.find_element(By.ID, "author")
            WebDriverWait(driver, 10).until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "#category option")) > 1)
            category_select = Select(driver.find_element(By.ID, "category"))
            category_select.select_by_index(1)
            barcode_input = driver.find_element(By.ID, "barcode")
            description_input = driver.find_element(By.ID, "description")
            file_input = driver.find_element(By.ID, "fileInput")
            image_input = driver.find_element(By.ID, "imageUpload1")
            print("TestUploadBook: Điền đầy đủ thông tin sách")
            title_input.send_keys("Test Book")
            author_input.send_keys("Test Author")
            barcode = str(random.randint(1000000000, 9999999999))
            barcode_input.send_keys(barcode)
            description_input.send_keys("This is a test book upload.")
            base_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
            pdf_path = os.path.join(base_dir, "Final-Report_SmartLib.pdf")
            image_path = os.path.join(base_dir, "img.png")
            file_input.send_keys(pdf_path)
            image_input.send_keys(image_path)
            print("TestUploadBook: Nộp form upload")
            driver.find_element(By.ID, "submitBtn").click()
            print("TestUploadBook: Đã bấm submit, chờ modal đóng...")
            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located((By.ID, "upload-book-container"))
            )
            print("TestUploadBook: Modal đã đóng, quay về trang chủ...")
            logo_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.logo#logo"))
            )
            logo_link.click()
            for _ in range(20):
                current_url = driver.current_url
                if "/homePage" in current_url:
                    print("TestUploadBook PASS: Upload sách thành công !")
                    return
                time.sleep(0.5)
            print("TestUploadBook FAIL: Không quay về trang chủ sau khi upload!")
            self.fail("Không quay về trang chủ sau khi upload!")
        except TimeoutException as e:
            print(f"TestUploadBook FAIL: Upload Book feature test timeout: {e}")
            self.fail("Timeout waiting during upload book feature test")

    def test_upload_book_file_not_pdf(self):
        """
        Kiểm tra upload file không phải PDF (ví dụ README.md)
        Mong muốn: Hiện thông báo "Only PDF files are allowed" và không lưu record.
        """
        try:
            print("Bắt đầu test upload file không phải PDF qua UI")
            self.login()
            driver = self.driver
            user_icon = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "user"))
            )
            ActionChains(driver).move_to_element(user_icon).perform()
            time.sleep(1)
            dropdown_items = driver.find_elements(By.XPATH, "//li")
            found = False
            for item in dropdown_items:
                if "my uploaded book" in item.text.strip().lower():
                    item.click()
                    found = True
                    break
            if not found:
                print("FAIL: Không tìm thấy mục 'My Uploaded Book' trong dropdown!")
                self.fail("Không tìm thấy mục 'My Uploaded Book' trong dropdown!")
            for _ in range(20):
                if "/myUploadedBookPage" in driver.current_url:
                    break
                time.sleep(0.5)
            else:
                print("FAIL: Không chuyển sang giao diện My Uploaded Book!")
                self.fail("Không chuyển sang giao diện My Uploaded Book!")
            upload_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "upload_book"))
            )
            upload_btn.click()
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "upload-book-container"))
            )
            title_input = driver.find_element(By.ID, "title")
            author_input = driver.find_element(By.ID, "author")
            WebDriverWait(driver, 10).until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "#category option")) > 1)
            category_select = Select(driver.find_element(By.ID, "category"))
            category_select.select_by_index(1)
            barcode_input = driver.find_element(By.ID, "barcode")
            description_input = driver.find_element(By.ID, "description")
            file_input = driver.find_element(By.ID, "fileInput")
            image_input = driver.find_element(By.ID, "imageUpload1")
            title_input.send_keys("Test Book Not PDF")
            author_input.send_keys("Test Author")
            barcode = str(random.randint(1000000000, 9999999999))
            barcode_input.send_keys(barcode)
            description_input.send_keys("This is a test book upload with non-pdf file.")
            base_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
            not_pdf_path = os.path.join(base_dir, "README.md")
            image_path = os.path.join(base_dir, "img.png")
            file_input.send_keys(not_pdf_path)
            image_input.send_keys(image_path)
            print("Nộp form upload với file không phải PDF")
            driver.find_element(By.ID, "submitBtn").click()
            try:
                alert = WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Only PDF files are allowed') or contains(text(), 'PDF')]"))
                )
                print("PASS: Hiện thông báo 'Only PDF files are allowed' khi upload file không phải PDF!")
            except TimeoutException:
                # Nếu không hiện thông báo lỗi, kiểm tra có upload thành công không
                print("FAIL: Không hiện thông báo 'Only PDF files are allowed' khi upload file không phải PDF!")
                # Thử quay về trang chủ nếu upload thành công (bị lỗi hệ thống)
                try:
                    logo_link = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.logo#logo"))
                    )
                    logo_link.click()
                    for _ in range(20):
                        current_url = driver.current_url
                        if "/homePage" in current_url:
                            print("FAIL: Hệ thống vẫn cho upload file không phải PDF và quay về trang chủ!")
                            self.fail("Hệ thống vẫn cho upload file không phải PDF!")
                        time.sleep(0.5)
                except Exception:
                    pass
                self.fail("Không hiện thông báo 'Only PDF files are allowed' khi upload file không phải PDF!")
        except Exception as e:
            print(f"FAIL: Lỗi khi test upload file không phải PDF: {e}")
            self.fail(f"Lỗi khi test upload file không phải PDF: {e}")

    def test_upload_book_title_too_long(self):
        """
        Kiểm tra giới hạn ký tự của Book Title: nhập 250 ký tự, mong muốn không cho submit, hiện thông báo lỗi, không lưu record.
        """
        try:
            print("Bắt đầu test giới hạn ký tự Book Title (quá 200 ký tự)")
            self.login()
            driver = self.driver
            user_icon = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "user"))
            )
            ActionChains(driver).move_to_element(user_icon).perform()
            time.sleep(1)
            dropdown_items = driver.find_elements(By.XPATH, "//li")
            found = False
            for item in dropdown_items:
                if "my uploaded book" in item.text.strip().lower():
                    item.click()
                    found = True
                    break
            if not found:
                print("FAIL: Không tìm thấy mục 'My Uploaded Book' trong dropdown!")
                self.fail("Không tìm thấy mục 'My Uploaded Book' trong dropdown!")
            for _ in range(20):
                if "/myUploadedBookPage" in driver.current_url:
                    break
                time.sleep(0.5)
            else:
                print("FAIL: Không chuyển sang giao diện My Uploaded Book!")
                self.fail("Không chuyển sang giao diện My Uploaded Book!")
            upload_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "upload_book"))
            )
            upload_btn.click()
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "upload-book-container"))
            )
            # Nhập Book Title vượt quá 200 ký tự
            title_input = driver.find_element(By.ID, "title")
            long_title = "A" * 260
            title_input.send_keys(long_title)
            author_input = driver.find_element(By.ID, "author")
            WebDriverWait(driver, 10).until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "#category option")) > 1)
            category_select = Select(driver.find_element(By.ID, "category"))
            category_select.select_by_index(1)
            barcode_input = driver.find_element(By.ID, "barcode")
            description_input = driver.find_element(By.ID, "description")
            file_input = driver.find_element(By.ID, "fileInput")
            image_input = driver.find_element(By.ID, "imageUpload1")
            author_input.send_keys("Test Author")
            barcode = str(random.randint(1000000000, 9999999999))
            barcode_input.send_keys(barcode)
            description_input.send_keys("Test book title too long.")
            base_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
            pdf_path = os.path.join(base_dir, "Final-Report_SmartLib.pdf")
            image_path = os.path.join(base_dir, "img.png")
            file_input.send_keys(pdf_path)
            image_input.send_keys(image_path)
            print("Nộp form upload với Book Title quá 200 ký tự")
            driver.find_element(By.ID, "submitBtn").click()
            # Kiểm tra alert popup nếu có
            try:
                WebDriverWait(driver, 3).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert_text = alert.text
                if "Book Title must be" in alert_text or "≤ 200 characters" in alert_text or "200 ký tự" in alert_text:
                    print("PASS: Hiện thông báo 'Book Title must be ≤ 200 characters' khi nhập quá 200 ký tự!")
                    alert.accept()
                elif "value too long" in alert_text or "character varying" in alert_text:
                    print(f"FAIL: Hệ thống trả về lỗi kỹ thuật DB: {alert_text}")
                    alert.accept()
                    self.fail("Hệ thống trả về lỗi kỹ thuật DB thay vì thông báo người dùng!")
                else:
                    print(f"FAIL: Alert không đúng nội dung mong muốn: {alert_text}")
                    alert.accept()
                    self.fail(f"Alert không đúng nội dung mong muốn: {alert_text}")
            except TimeoutException:
                print("FAIL: Không hiện alert khi nhập quá 200 ký tự!")
                # Thử quay về trang chủ nếu hệ thống vẫn cho submit
                try:
                    logo_link = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.logo#logo"))
                    )
                    logo_link.click()
                    for _ in range(20):
                        current_url = driver.current_url
                        if "/homePage" in current_url:
                            print("FAIL: Hệ thống vẫn cho upload Book Title quá 200 ký tự và quay về trang chủ!")
                            self.fail("Hệ thống vẫn cho upload Book Title quá 200 ký tự!")
                        time.sleep(0.5)
                except Exception:
                    pass
                self.fail("Không hiện thông báo khi nhập quá 200 ký tự!")
        except Exception as e:
            print(f"FAIL: Lỗi khi test upload Book Title quá 200 ký tự: {e}")
            self.fail(f"Lỗi khi test upload Book Title quá 200 ký tự: {e}")

if __name__ == '__main__':
    unittest.main()
