import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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
        driver.get(f"{self.base_url}/login")
        driver.find_element(By.ID, "email").send_keys("phamhuyhoa03@gmail.com")
        driver.find_element(By.ID, "password").send_keys("huyhoa10102003")
        driver.find_element(By.ID, "login").click()
        WebDriverWait(driver, 10).until(lambda d: "/login" not in d.current_url)

    def search_from_header(self, keyword):
        driver = self.driver
        search_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "search-input"))
        )
        search_input.clear()
        search_input.send_keys(keyword)
        try:
            search_btn = driver.find_element(By.ID, "search-btn")
            search_btn.click()
        except Exception:
            from selenium.webdriver.common.keys import Keys
            search_input.send_keys(Keys.ENTER)
        try:
            WebDriverWait(driver, 5).until(lambda d: "/search" in d.current_url)
        except Exception:
            pass

    def test_search_empty_query_show_all(self):
        print("TestSearchBook: Bắt đầu test tìm kiếm rỗng (ra toàn bộ sách)")
        self.login()
        driver = self.driver
        driver.get(f"{self.base_url}/")
        self.search_from_header("")
        all_books = driver.find_elements(By.CSS_SELECTOR, ".book-item")
        if len(all_books) > 0:
            print(f"TestSearchBook PASS: Tìm kiếm rỗng hiển thị {len(all_books)} sách!")
        else:
            print("TestSearchBook FAIL: Không có sách nào được hiển thị khi tìm kiếm rỗng!")
            self.fail("Không có sách nào được hiển thị khi tìm kiếm rỗng!")

    def test_search_by_category(self):
        print("TestSearchBook: Bắt đầu test tìm kiếm theo danh mục")
        self.login()
        driver = self.driver
        driver.get(f"{self.base_url}/")
        self.search_from_header("")
        category_select = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "category"))
        )
        from selenium.webdriver.support.ui import Select
        select = Select(category_select)
        select.select_by_index(1)
        filter_btn = driver.find_element(By.ID, "filter")
        filter_btn.click()
        selected_category = select.first_selected_option.text
        WebDriverWait(driver, 10).until(lambda d: len(d.find_elements(By.CSS_SELECTOR, ".book-item")) > 0)
        books = driver.find_elements(By.CSS_SELECTOR, ".book-item")
        all_in_category = all(selected_category in book.text for book in books)
        if all_in_category and len(books) > 0:
            print(f"TestSearchBook PASS: Tìm kiếm theo danh mục '{selected_category}' ra {len(books)} sách đúng danh mục!")
        else:
            print(f"TestSearchBook FAIL: Có sách không thuộc danh mục '{selected_category}' hoặc không có sách!")
            self.fail(f"Có sách không thuộc danh mục '{selected_category}' hoặc không có sách!")

    def test_search_by_first_two_letters(self):
        print("TestSearchBook: Bắt đầu test tìm kiếm theo 2 ký tự đầu tên sách với từ khóa 'Test'")
        self.login()
        driver = self.driver
        driver.get(f"{self.base_url}/")
        self.search_from_header("Test")
        books = driver.find_elements(By.CSS_SELECTOR, ".book-item")
        if any("Test".lower() in b.text.lower() for b in books):
            print("TestSearchBook PASS: Tìm kiếm 2 ký tự đầu tên sách ra kết quả!")
        else:
            print("TestSearchBook FAIL: Không tìm thấy sách với 2 chữ cái đầu!")
            self.fail("Không tìm thấy sách với 2 chữ cái đầu!")

    def test_search_by_author(self):
        print("TestSearchBook: Bắt đầu test tìm kiếm theo tên tác giả 'Test'")
        self.login()
        driver = self.driver
        driver.get(f"{self.base_url}/")
        author_name = "Test"
        self.search_from_header(author_name)
        books = driver.find_elements(By.CSS_SELECTOR, ".book-item")
        if any(author_name.lower() in b.text.lower() for b in books):
            print("TestSearchBook PASS: Tìm kiếm theo tên tác giả ra kết quả!")
        else:
            print("TestSearchBook FAIL: Không tìm thấy sách theo tên tác giả!")
            self.fail("Không tìm thấy sách theo tên tác giả!")

    def test_search_with_filter(self):
        print("TestSearchBook: Bắt đầu test lọc danh sách tìm kiếm bằng filter (Most-Viewed)")
        self.login()
        driver = self.driver
        driver.get(f"{self.base_url}/")
        self.search_from_header("Test")
        sort_select = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "sorting_way"))
        )
        from selenium.webdriver.support.ui import Select
        select = Select(sort_select)
        select.select_by_value("reviewed")
        filter_btn = driver.find_element(By.ID, "filter")
        filter_btn.click()
        books = driver.find_elements(By.CSS_SELECTOR, ".book-item")
        if len(books) > 0:
            print(f"TestSearchBook PASS: Lọc filter Most-Viewed ra {len(books)} sách!")
        else:
            print("TestSearchBook FAIL: Không có sách nào sau khi lọc!")
            self.fail("Không có sách nào sau khi lọc!")

if __name__ == '__main__':
    unittest.main()
