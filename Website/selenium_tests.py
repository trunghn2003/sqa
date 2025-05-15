import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

class SeleniumTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize Chrome WebDriver with absolute path to chromedriver.exe
        chromedriver_path = r"D:\Ky 2 nam 4\SQA\sqa\chromedriver.exe"
        service = Service(executable_path=chromedriver_path)
        cls.driver = webdriver.Chrome(service=service)
        cls.base_url = "http://localhost:8000"

    @classmethod
    def tearDownClass(cls):
        # Quit the browser
        cls.driver.quit()

    def login(self, username="phamhuyhoa03@gmail.com", password="huyhoa10102003"):
        """Helper function to log in a user before running tests that require authentication."""
        driver = self.driver
        driver.get(f"{self.base_url}/login/")
        driver.find_element(By.NAME, "email").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    def test_read_book(self):
        """Test reading a book from the book list."""
        driver = self.driver
        driver.get(f"{self.base_url}/books/")
        # Click on first book
        book_link = driver.find_element(By.CSS_SELECTOR, ".book-item a")
        book_link.click()
        # Verify that book detail page is displayed
        self.assertIn("/books/", driver.current_url)

    def test_upload_book(self):
        """Test uploading a new book (requires login)."""
        self.login()
        driver = self.driver
        driver.get(f"{self.base_url}/books/upload/")
        title_input = driver.find_element(By.NAME, "title")
        file_input = driver.find_element(By.NAME, "file")
        title_input.send_keys("Test Book")
        file_input.send_keys(r"D:\\Ky 2 nam 4\\SQA\\sqa\\img.png")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        success = driver.find_element(By.CLASS_NAME, "alert-success")
        self.assertTrue(success.is_displayed())

    def test_manage_book(self):
        """Test managing books (delete from the list, requires login)."""
        self.login()
        driver = self.driver
        driver.get(f"{self.base_url}/books/manage/")
        delete_btn = driver.find_element(By.CSS_SELECTOR, ".delete-book")
        delete_btn.click()
        alert = driver.switch_to.alert
        alert.accept()
        self.assertNotIn("Test Book", driver.page_source)

    def test_rate_book(self):
        """Test rating a book (requires login)."""
        self.login()
        driver = self.driver
        driver.get(f"{self.base_url}/books/1/")
        star = driver.find_element(By.CSS_SELECTOR, ".star-rating input[value='5']")
        star.click()
        driver.find_element(By.CSS_SELECTOR, "button.submit-rating").click()
        rating = driver.find_element(By.CLASS_NAME, "current-rating")
        self.assertIn("5", rating.text)

    def test_search_book(self):
        """Test searching for a book (requires login)."""
        self.login()
        driver = self.driver
        driver.get(f"{self.base_url}/books/?search=Test")
        results = driver.find_elements(By.CSS_SELECTOR, ".book-item")
        self.assertTrue(any("Test" in r.text for r in results))

if __name__ == '__main__':
    unittest.main()
