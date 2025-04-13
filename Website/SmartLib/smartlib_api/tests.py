from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from rest_framework import status
from django.utils.timezone import now
import bcrypt
from .models import User, Reader, Gamification_Record, Notification, Book, Rating_And_Review, Category, Manager
from .views import AddRatingAndReviewView
from unittest.mock import patch, PropertyMock

# class UserLoginViewTests(APITestCase):
#     def setUp(self):
#         # Create test user
#         self.client = APIClient()
#         self.login_url = reverse('login-api')  # Fixed URL pattern
        
#         # Create a test user with bcrypt hashed password
#         password = "testpassword123"
#         hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
#         self.user = User.objects.create(
#             user_name="Test User",  # Added required field
#             email="test@example.com",
#             user_password=hashed.decode('utf-8'),
#             is_active=True,
#             last_login=None
#         )
        
#         # Create associated reader
#         self.reader = Reader.objects.create(
#             user_id=self.user.user_id,
#             reader_point=0,
#             reader_rank="New",
#             is_first_time=True
#         )

#         # Create test book with required fields
#         self.book = Book.objects.create(
#             book_name="Test Book",
#             book_author="Test Author",
#             book_type="Fiction",
#             book_barcode="123456789",
#             book_description="Test Description",
#             category_id=1,  # Assuming category with ID 1 exists
#             status=Book.Status.ACCEPTED
#         )

#     def test_successful_login(self):
#         """Test successful login with correct credentials"""
#         data = {
#             'email': 'test@example.com',
#             'user_password': 'testpassword123'
#         }
#         response = self.client.post(self.login_url, data, format='json')
        
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn('jwt', response.data)
#         self.assertIn('isDailyLogin', response.data)
#         self.assertTrue(response.data['isDailyLogin'])

#     def test_login_with_wrong_password(self):
#         """Test login with incorrect password"""
#         data = {
#             'email': 'test@example.com',
#             'user_password': 'wrongpassword'
#         }
#         response = self.client.post(self.login_url, data, format='json')
        
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_login_with_nonexistent_user(self):
#         """Test login with non-existent user"""
#         data = {
#             'email': 'nonexistent@example.com',
#             'user_password': 'testpassword123'
#         }
#         response = self.client.post(self.login_url, data, format='json')
        
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_login_inactive_user(self):
#         """Test login with inactive user account"""
#         self.user.is_active = False
#         self.user.save()
        
#         data = {
#             'email': 'test@example.com',
#             'user_password': 'testpassword123'
#         }
#         response = self.client.post(self.login_url, data, format='json')
        
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_daily_login_points(self):
#         """Test if points are awarded for daily login"""
#         data = {
#             'email': 'test@example.com',
#             'user_password': 'testpassword123'
#         }
        
#         # First login
#         response = self.client.post(self.login_url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
        
#         # Check if reader points were updated
#         reader = Reader.objects.get(user_id=self.user.user_id)
#         self.assertEqual(reader.reader_point, 10)
        
#         # Check if gamification record was created
#         gamification = Gamification_Record.objects.filter(
#             reader_id=reader.reader_id,
#             gamification_description="Daily login"
#         ).exists()
#         self.assertTrue(gamification)
        
#         # Check if notification was created
#         notification = Notification.objects.filter(
#             reader_id=reader.reader_id,
#             notification_title="New Point Achievement"
#         ).exists()
#         self.assertTrue(notification)

#     def test_reader_rank_update(self):
#         """Test reader rank updates based on points"""
#         # Set initial points close to Bronze rank
#         self.reader.reader_point = 495
#         self.reader.save()
        
#         data = {
#             'email': 'test@example.com',
#             'user_password': 'testpassword123'
#         }
        
#         # Login to get +10 points (total 505)
#         response = self.client.post(self.login_url, data, format='json')
        
#         # Check if rank was updated to Bronze
#         reader = Reader.objects.get(user_id=self.user.user_id)
#         self.assertEqual(reader.reader_rank, "Bronze")
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from rest_framework import status
from django.utils.timezone import now
import bcrypt
from .models import User, Reader, Gamification_Record, Notification, Book, Rating_And_Review, Category, Manager
from .views import AddRatingAndReviewView
from unittest.mock import patch, PropertyMock
# Run test command: python manage.py test smartlib_api.tests.AddRatingAndReviewViewTests -v 2
# Run coverage command: coverage run manage.py test smartlib_api.tests.AddRatingAndReviewViewTests -v 2
# Run coverage report: coverage report -m
# Run .venv command: .venv/Scripts/activate
class AddRatingAndReviewViewTests(APITestCase):
    # Khi dùng unittest trong python sẽ tự chạy csdl mock để kiểm thử không bị lỗi nên ta cần hàm setUp để khởi tạo các biến cho csdl mock này
    # Hoàn toàn có thể tạo các biến cho csdl mock này trong các hàm test nhưng để tiện lợi ta dùng hàm setUp
    def setUp(self):
        # Tao user va reader de test
        self.factory = APIRequestFactory()
        self.view = AddRatingAndReviewView.as_view()
        self.add_review_url = reverse('insertRatingAndReview')
        
        # Tao category de test
        self.category = Category.objects.create(
            category_id=1,
            category_name="Test Category"
        )
        
        # Tao manager
        self.manager_user = User.objects.create(
            user_name="Test Manager",
            email="manager@example.com",
            user_password="$2b$12$2.302RNsA8cEA6QHXpuJMun5mR/.hsGSuSwMxFTG4rfiEmiViu1/W",
            is_active=True
        )
        
        self.manager = Manager.objects.create(
            manager_id=2,
            user=self.manager_user
        )
        
        # Tao reader
        self.user = User.objects.create(
            user_name="tienngo",
            email="tienclone36@gmail.com",
            user_password="$2b$12$2.302RNsA8cEA6QHXpuJMun5mR/.hsGSuSwMxFTG4rfiEmiViu1/W",
            is_active=True
        )
        
        self.reader = Reader.objects.create(
            user_id=self.user.user_id,
            reader_point=0,
            reader_rank="New"
        )
        
        # Tao test book
        self.book = Book.objects.create(
            book_name="Test Book",
            book_author="Test Author",
            book_type="Fiction",
            book_barcode="123456789",
            book_description="Test Description",
            category=self.category,
            status=Book.Status.ACCEPTED
        )

    def test_successful_review_addition(self):
        """
        Test Case ID: RAR-001
        Mo ta: Test them danh gia va review thanh cong
        Mong doi: Review duoc tao, diem duoc cap nhat, thong bao duoc gui
        """
        print("\n=== Starting test_successful_review_addition ===")
        #Kiem tra so luong review ban dau
        initial_review_count = Rating_And_Review.objects.count()
        #Kiem tra diem ban dau
        initial_points = self.reader.reader_point
        print(f"Initial review count: {initial_review_count}")
        print(f"Initial reader points: {initial_points}")
        #Tao du lieu gui len
        data = {
            'book_id': self.book.pk,
            'user_id': self.reader.user_id,
            'rating': 5,
            'review': 'Tuyet voi ong mat troi'
        }
        print(f"Sending request with data: {data}")
        
        # Tạo và gửi request qua APIRequestFactory
        request = self.factory.post(self.add_review_url, data, format='json')
        response = self.view(request)
        print(f"Response status code: {response.status_code}")
        print(f"Response data: {response.data}")
        
        print("\n=== Evaluating test_successful_review_addition ===")
        # Kiem tra response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 
                        "Response status code should be 201 Created")
        
        # Kiem tra trang thai database
        final_review_count = Rating_And_Review.objects.count()
        self.assertEqual(final_review_count, initial_review_count + 1,
                        f"Review count should increase by 1 (was {initial_review_count}, now {final_review_count})")
        
        new_review = Rating_And_Review.objects.first()
        self.assertEqual(new_review.rating, 5,
                        f"Rating should be 5, got {new_review.rating}")
        self.assertEqual(new_review.review, 'Tuyet voi ong mat troi',
                        f"Review text should be 'Tuyet voi ong mat troi', got '{new_review.review}'")
        
        # Kiem tra cap nhat diem
        reader = Reader.objects.get(user_id=self.reader.user_id)
        final_points = reader.reader_point
        self.assertEqual(final_points, initial_points + 20,
                        f"Reader points should increase by 20 (was {initial_points}, now {final_points})")
        
        # Kiem tra gamification record
        gamification_record = Gamification_Record.objects.filter(
            reader_id=reader.reader_id,
            gamification_description="Rating And Review Book Achievement"
        ).first()
        self.assertIsNotNone(gamification_record,
                           "Gamification record should be created")
        self.assertEqual(gamification_record.achieved_point, 20,
                        f"Gamification points should be 20, got {gamification_record.achieved_point}")
        
        # Kiem tra notification
        notification = Notification.objects.filter(
            reader_id=reader.reader_id,
            notification_title="New Point Achievement"
        ).first()
        self.assertIsNotNone(notification,
                           "Notification should be created")
        self.assertEqual(notification.notification_record, "+20 Point for Rating And Review Book",
                        f"Notification message should be '+20 Point for Rating And Review Book', got '{notification.notification_record}'")
        
        print("=== Test completed successfully ===\n")

    def test_missing_fields(self):
        """
        Test Case ID: RAR-002
        Mo ta: Test gui review thieu truong bat buoc
        Mong doi: Tra ve 400 Bad Request
        """
        initial_review_count = Rating_And_Review.objects.count()
        
        data = {
            'book_id': self.book.pk,
            'user_id': self.reader.user_id,
            'rating': 5
            # Thieu truong 'review'
        }
        
        request = self.factory.post(self.add_review_url, data, format='json')
        response = self.view(request)
        
        # Kiem tra response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        
        # Kiem tra trang thai database (khong duoc thay doi)
        self.assertEqual(Rating_And_Review.objects.count(), initial_review_count)

    def test_nonexistent_book(self):
        """
        Test Case ID: RAR-003
        Mo ta: Test gui review cho sach khong ton tai
        Mong doi: Tra ve 404 Not Found
        """
        initial_review_count = Rating_And_Review.objects.count()
        
        data = {
            'book_id': 999,  # ID sach khong ton tai
            'user_id': self.reader.user_id,
            'rating': 5,
            'review': 'Tuyet voi ong mat troi'
        }
        
        request = self.factory.post(self.add_review_url, data, format='json')
        response = self.view(request)
        
        # Kiem tra response
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
        
        # Kiem tra trang thai database (khong duoc thay doi)
        self.assertEqual(Rating_And_Review.objects.count(), initial_review_count)

    def test_nonexistent_reader(self):
        """
        Test Case ID: RAR-004
        Mo ta: Test gui review boi nguoi doc khong ton tai
        Mong doi: Tra ve 404 Not Found
        """
        initial_review_count = Rating_And_Review.objects.count()
        
        data = {
            'book_id': self.book.pk,
            'user_id': 999,  # ID nguoi doc khong ton tai
            'rating': 5,
            'review': 'Tuyet voi ong mat troi'
        }
        
        request = self.factory.post(self.add_review_url, data, format='json')
        response = self.view(request)
        
        # Kiem tra response
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
        
        # Kiem tra trang thai database (khong duoc thay doi)
        self.assertEqual(Rating_And_Review.objects.count(), initial_review_count)

    def test_duplicate_review(self):
        """
        Test Case ID: RAR-005
        Mo ta: Test gui nhieu review boi cung mot nguoi cho cung mot sach
        Mong doi: Lan gui thu hai se that bai voi 400 Bad Request
        """
        initial_review_count = Rating_And_Review.objects.count()
        
        # Lan review dau tien
        data = {
            'book_id': self.book.pk,
            'user_id': self.reader.user_id,
            'rating': 5,
            'review': 'First review'
        }
        
        request = self.factory.post(self.add_review_url, data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Kiem tra trang thai database sau lan review dau tien
        self.assertEqual(Rating_And_Review.objects.count(), initial_review_count + 1)
        
        # Thu gui review lan hai
        data['review'] = 'Second review'
        request = self.factory.post(self.add_review_url, data, format='json')
        response = self.view(request)
        
        # Kiem tra response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        
        # Kiem tra trang thai database (khong duoc thay doi)
        self.assertEqual(Rating_And_Review.objects.count(), initial_review_count + 1)

    def test_review_pending_book(self):
        """
        Test Case ID: RAR-006
        Mo ta: Test gui review cho sach dang cho duyet
        Mong doi: Tra ve 400 Bad Request
        """
        initial_review_count = Rating_And_Review.objects.count()
        
        # Tao sach dang cho duyet
        pending_book = Book.objects.create(
            book_name="Pending Book",
            book_author="Test Author",
            book_type="Fiction",
            book_barcode="987654321",
            book_description="Test Description",
            category=self.category,
            status=Book.Status.PENDING
        )

        data = {
            'book_id': pending_book.pk,
            'user_id': self.reader.user_id,
            'rating': 5,
            'review': 'Tuyet voi ong mat troi'
        }
        
        request = self.factory.post(self.add_review_url, data, format='json')
        response = self.view(request)
        
        # Kiem tra response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        
        # Kiem tra trang thai database (khong duoc thay doi)
        self.assertEqual(Rating_And_Review.objects.count(), initial_review_count)

    def test_review_rejected_book(self):
        """
        Test Case ID: RAR-007
        Mo ta: Test gui review cho sach da bi tu choi
        Mong doi: Tra ve 400 Bad Request
        """
        initial_review_count = Rating_And_Review.objects.count()
        
        # Tao sach da bi tu choi
        rejected_book = Book.objects.create(
            book_name="Rejected Book",
            book_author="Test Author",
            book_type="Fiction",
            book_barcode="456789123",
            book_description="Test Description",
            category=self.category,
            status=Book.Status.REJECTED
        )

        data = {
            'book_id': rejected_book.pk,
            'user_id': self.reader.user_id,
            'rating': 5,
            'review': 'Tuyet voi ong mat troi'
        }
        
        request = self.factory.post(self.add_review_url, data, format='json')
        response = self.view(request)
        
        # Kiem tra response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        
        # Kiem tra trang thai database (khong duoc thay doi)
        self.assertEqual(Rating_And_Review.objects.count(), initial_review_count)

    def test_rating_range_validation_high(self):
        """
        Test Case ID: RAR-009
        Mo ta: Test gui review voi gia tri danh gia khong hop le
        Mong doi: Tra ve 400 Bad Request cho danh gia ngoai khoang 1-5
        """
        initial_review_count = Rating_And_Review.objects.count()
        
        # Test danh gia toi da
        data = {
            'book_id': self.book.pk,
            'user_id': self.reader.user_id,
            'rating': 6,  # Danh gia khong hop le
            'review': 'Tuyet voi ong mat troi'
        }
        
        request = self.factory.post(self.add_review_url, data, format='json')
        response = self.view(request)
        
        # Kiem tra response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        
        # Kiem tra trang thai database (khong duoc thay doi)
        self.assertEqual(Rating_And_Review.objects.count(), initial_review_count)

    def test_rating_range_validation_low(self):
        """
        Test Case ID: RAR-010
        Mo ta: Test gui review voi gia tri danh gia khong hop le
        Mong doi: Tra ve 400 Bad Request cho danh gia ngoai khoang 1-5
        """
        initial_review_count = Rating_And_Review.objects.count()
        
        # Test danh gia toi da
        data = {
            'book_id': self.book.pk,
            'user_id': self.reader.user_id,
            'rating': 0,  # Danh gia khong hop le
            'review': 'Tuyet voi ong mat troi'
        }
        
        request = self.factory.post(self.add_review_url, data, format='json')
        response = self.view(request)
        
        # Kiem tra response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
         
        # Kiem tra trang thai database (khong duoc thay doi)
        self.assertEqual(Rating_And_Review.objects.count(), initial_review_count)
        
    def test_invalid_data_types(self):
        """
        Test Case ID: RAR-011
        Mo ta: Test gui review voi kieu du lieu khong hop le
        Mong doi: Tra ve 400 Bad Request
        """
        data = {
            'book_id': "1",  # Cần là integer
            'user_id': "not_a_number",  # Cần là integer
            'rating': "5",  # Cần là integer
            'review': 123   # Cần là string
        }
        request = self.factory.post(self.add_review_url, data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  
    def test_empty_review(self):
        """
        Test Case ID: RAR-012
        Mo ta: Test gui review voi noi dung trong
        Mong doi: Tra ve 400 Bad Request
        """
        data = {
            'book_id': self.book.pk,
            'user_id': self.reader.user_id,
            'rating': 5,
            'review': ""  # Trường trống
        }
        request = self.factory.post(self.add_review_url, data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_review_too_long(self):
        """
        Test Case ID: RAR-013
        Mo ta: Test gui review voi noi dung qua dai
        Mong doi: Tra ve 400 Bad Request
        """
        data = {
            'book_id': self.book.pk,
            'user_id': self.reader.user_id,
            'rating': 5,
            'review': "a" * 256  # Trường review quá 255
        }
        request = self.factory.post(self.add_review_url, data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_concurrent_reviews(self):
        """
        Test Case ID: RAR-014
        Mo ta: Test gui nhieu review cung luc cho cung mot sach
        Mong doi: Chi mot review duoc tao
        """
        initial_review_count = Rating_And_Review.objects.count()
        
        # Tạo request
        data = {
            'book_id': self.book.pk,
            'user_id': self.reader.user_id,
            'rating': 5,
            'review': 'Concurrent review'
        }
        
        # Gửi nhiều request
        requests = [self.factory.post(self.add_review_url, data, format='json') for _ in range(5)]
        responses = [self.view(request) for request in requests]
        
        # Chỉ có 1 review được gửi đi
        self.assertEqual(Rating_And_Review.objects.count(), initial_review_count + 1)
    def test_book_deleted_during_review(self):
        """
        Test Case ID: RAR-015
        Mo ta: Test truong hop sach bi xoa trong khi dang gui review
        Mong doi: Tra ve 404 Not Found
        """
        data = {
            'book_id': self.book.pk,
            'user_id': self.reader.user_id,
            'rating': 3,
            'review': 'Test review'
        }

        # Xóa sách sau khi tạo request nhưng trước khi xử lý
        request = self.factory.post(self.add_review_url, data, format='json')
        self.book.delete()
        
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)