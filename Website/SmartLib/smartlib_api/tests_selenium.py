from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.contrib.auth import get_user_model
import time

User = get_user_model()

class SeleniumSmartLibTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('disable-gpu')
        # ensure chromedriver is in PATH or specify executable_path
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    @classmethod
    def setUpTestData(cls):
        # create a test user and a test book
        cls.user = User.objects.create_user(username='testuser', password='password')
        from .models import Book
        cls.book = Book.objects.create(title='Test Book', author='Author', description='Sample', file_url='')

    def login(self):
        self.driver.get(f'{self.live_server_url}/login/')
        self.driver.find_element(By.NAME, 'username').send_keys('testuser')
        self.driver.find_element(By.NAME, 'password').send_keys('password')
        self.driver.find_element(By.CSS_SELECTOR, 'button[type=submit]').click()
        time.sleep(1)

    def test_read_book(self):
        # user visits book reading page
        self.login()
        self.driver.get(f'{self.live_server_url}/books/{self.book.id}/read/')
        content = self.driver.find_element(By.CSS_SELECTOR, '.book-content')
        self.assertIn('Test Book', content.text)

    def test_upload_book(self):
        # user uploads a new book
        self.login()
        self.driver.get(f'{self.live_server_url}/books/upload/')
        self.driver.find_element(By.NAME, 'title').send_keys('New Book')
        self.driver.find_element(By.NAME, 'author').send_keys('Author2')
        self.driver.find_element(By.NAME, 'description').send_keys('Upload test')
        # skip file upload in headless test or mock it
        self.driver.find_element(By.CSS_SELECTOR, 'button[type=submit]').click()
        time.sleep(1)
        self.assertIn('/books/', self.driver.current_url)

    def test_manage_books_list(self):
        # manager page listing books
        self.login()
        self.driver.get(f'{self.live_server_url}/admin/books/')
        table = self.driver.find_element(By.ID, 'books-table')
        self.assertTrue(table.is_displayed())

    def test_rate_book(self):
        # user rates a book
        self.login()
        self.driver.get(f'{self.live_server_url}/books/{self.book.id}/')
        stars = self.driver.find_elements(By.CSS_SELECTOR, '.star')
        stars[4].click()  # click 5th star
        self.driver.find_element(By.NAME, 'review').send_keys('Great read!')
        self.driver.find_element(By.CSS_SELECTOR, 'button.submit-review').click()
        time.sleep(1)
        reviews = self.driver.find_elements(By.CSS_SELECTOR, '.review-item')
        self.assertTrue(any('Great read!' in r.text for r in reviews))

    def test_search_books(self):
        # user searches for a book
        self.login()
        self.driver.get(f'{self.live_server_url}/search/')
        search_input = self.driver.find_element(By.NAME, 'q')
        search_input.send_keys('Test Book')
        search_input.send_keys(Keys.RETURN)
        time.sleep(1)
        results = self.driver.find_elements(By.CSS_SELECTOR, '.search-result')
        self.assertTrue(any('Test Book' in r.text for r in results))
