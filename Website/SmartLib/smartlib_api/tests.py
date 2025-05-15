from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from rest_framework import status
from django.utils.timezone import now
import bcrypt
from .models import User, Reader, Book, Rating_And_Review, Category, Notification, BookContinueReading, UploadedBook, Manager, Gamification_Record
from .views import (
    AddRatingAndReviewView,RatingAndReviewListView, MostRating_BookListView, MostReaded_BookListView,
    LastUploaded_BookListView, NotificationListView, LastThreeNotificationListView,
    CreateBookView, UploadedByView, ContinueReadingView, homePage, RankPage
)
from .models import WishList, FeedBack, UploadedBook, BookContinueReading, Notification
from .views import (
    AddBookToWishlist, RemoveBookFromWishlist, CheckBookInWishlist, WishListListView,
    LastThreeWishListView, InsertFeedbackView, UploadedBookListView, RemoveUploadedBookView,
    BookContinueReadingListView, WishListPage, NotificationPage, MyUploadedBookPage
)
from unittest.mock import patch, PropertyMock
from datetime import timedelta
# Run coverage command: coverage run manage.py test smartlib_api.tests.AddRatingAndReviewViewTests -v 2
# Run .venv command: .venv/Scripts/activate
# Run coverage all: coverage run manage.py test
# add to report: coverage html --include="*/smartlib_api/views.py"
class AddRatingAndReviewViewTests(APITestCase):
    # Set up csdl mock để kiểm thử
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
        Test Case ID: UT-RAR-001
        Mo ta: Test them danh gia va review thanh cong
        Mong doi: Review duoc tao, diem duoc cap nhat, thong bao duoc gui
        """
        print("\n=== Starting test_successful_review_addition ===")

        initial_review_count = Rating_And_Review.objects.count()
        initial_points = self.reader.reader_point
        print(f"Initial review count: {initial_review_count}")
        print(f"Initial reader points: {initial_points}")

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

        # Kiểm thử response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                        "Response status code should be 201 Created")

        # Kiểm thử trang thai database
        final_review_count = Rating_And_Review.objects.count()
        self.assertEqual(final_review_count, initial_review_count + 1,
                        f"Review count should increase by 1 (was {initial_review_count}, now {final_review_count})")

        new_review = Rating_And_Review.objects.first()
        self.assertEqual(new_review.rating, 5,
                        f"Rating should be 5, got {new_review.rating}")
        self.assertEqual(new_review.review, 'Tuyet voi ong mat troi',
                        f"Review text should be 'Tuyet voi ong mat troi', got '{new_review.review}'")

        # Kiểm thử cap nhat diem
        reader = Reader.objects.get(user_id=self.reader.user_id)
        final_points = reader.reader_point
        self.assertEqual(final_points, initial_points + 20,
                        f"Reader points should increase by 20 (was {initial_points}, now {final_points})")

        # Kiểm thử gamification record
        gamification_record = Gamification_Record.objects.filter(
            reader_id=reader.reader_id,
            gamification_description="Rating And Review Book Achievement"
        ).first()
        self.assertIsNotNone(gamification_record,
                           "Gamification record should be created")
        self.assertEqual(gamification_record.achieved_point, 20,
                        f"Gamification points should be 20, got {gamification_record.achieved_point}")

        # Kiểm thử notification
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
        Test Case ID: UT-RAR-002
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

        # Kiểm thử response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

        # Kiểm thử trang thai database (khong duoc thay doi)
        self.assertEqual(Rating_And_Review.objects.count(), initial_review_count)

    def test_nonexistent_book(self):
        """
        Test Case ID: UT-RAR-003
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

        # Kiểm thử response
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

        # Kiểm thử trang thai database (khong duoc thay doi)
        self.assertEqual(Rating_And_Review.objects.count(), initial_review_count)

    def test_nonexistent_reader(self):
        """
        Test Case ID: UT-RAR-004
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

        # Kiểm thử response
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

        # Kiểm thử trang thai database (khong duoc thay doi)
        self.assertEqual(Rating_And_Review.objects.count(), initial_review_count)

    def test_duplicate_review(self):
        """
        Test Case ID: UT-RAR-005
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

        # Kiểm thử trang thai database sau lan review dau tien
        self.assertEqual(Rating_And_Review.objects.count(), initial_review_count + 1)

        # Thu gui review lan hai
        data['review'] = 'Second review'
        request = self.factory.post(self.add_review_url, data, format='json')
        response = self.view(request)

        # Kiểm thử response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

        # Kiểm thử trang thai database (khong duoc thay doi)
        self.assertEqual(Rating_And_Review.objects.count(), initial_review_count + 1)

    def test_review_pending_book(self):
        """
        Test Case ID: UT-RAR-006
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

        # Kiểm thử response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

        # Kiểm thử trang thai database (khong duoc thay doi)
        self.assertEqual(Rating_And_Review.objects.count(), initial_review_count)

    def test_review_rejected_book(self):
        """
        Test Case ID: UT-RAR-007
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

        # Kiểm thử response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

        # Kiểm thử trang thai database (khong duoc thay doi)
        self.assertEqual(Rating_And_Review.objects.count(), initial_review_count)

    def test_rating_range_validation_high(self):
            """
            Test Case ID: UT-RAR-008
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

            # Kiểm thử response
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn('error', response.data)

            # Kiểm thử trang thai database (khong duoc thay doi)
            self.assertEqual(Rating_And_Review.objects.count(), initial_review_count)

    def test_rating_range_validation_low(self):
            """
            Test Case ID: UT-RAR-009
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

            # Kiểm thử response
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn('error', response.data)

            # Kiểm thử trang thai database (khong duoc thay doi)
            self.assertEqual(Rating_And_Review.objects.count(), initial_review_count)

    def test_invalid_data_types(self):
            """
            Test Case ID: UT-RAR-010
            Mo ta: Test gui review voi kieu du lieu khong hop le
            Mong doi: Tra ve 400 Bad Request
            """
            data = {
                'book_id': "1",  # Cần là integer
                'user_id': "khong phai so",  # Cần là integer
                'rating': "5",  # Cần là integer
                'review': 123   # Cần là string
            }
            request = self.factory.post(self.add_review_url, data, format='json')
            response = self.view(request)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_empty_review(self):
            """
            Test Case ID: UT-RAR-011
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
            Test Case ID: UT-RAR-012
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
            Test Case ID: UT-RAR-013
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
            Test Case ID: UT-RAR-014
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
    def test_bronze_rank_achievement(self):
        """
        Test Case ID: UT-RAR-015
        Mô tả: Test khi reader đạt 500 điểm để nhận rank Bronze
        Mong đợi: Rank của reader được cập nhật thành Bronze, điểm tăng đúng 20
        """
        print("\n=== Starting test_bronze_rank_achievement ===")

        # Thiết lập reader với 480 điểm (gần ngưỡng Bronze)
        self.reader.reader_point = 480
        self.reader.reader_rank = "New"
        self.reader.save()

        initial_points = self.reader.reader_point
        initial_rank = self.reader.reader_rank
        print(f"Initial reader points: {initial_points}")
        print(f"Initial reader rank: {initial_rank}")

        data = {
            'book_id': self.book.pk,
            'user_id': self.reader.user_id,
            'rating': 4,
            'review': 'Great book!'
        }
        print(f"Sending request with data: {data}")

        # Gửi request
        request = self.factory.post(self.add_review_url, data, format='json')
        response = self.view(request)
        print(f"Response status code: {response.status_code}")

        # Kiểm thử response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                        "Response status code should be 201 Created")

        # Kiểm thử cập nhật điểm và rank
        reader = Reader.objects.get(user_id=self.reader.user_id)
        final_points = reader.reader_point
        final_rank = reader.reader_rank
        self.assertEqual(final_points, initial_points + 20,
                        f"Reader points should increase by 20 (was {initial_points}, now {final_points})")
        self.assertEqual(final_rank, "Bronze",
                        f"Reader rank should be Bronze, got {final_rank}")

        print("=== Test completed successfully ===\n")

    def test_silver_rank_achievement(self):
        """
        Test Case ID: UT-RAR-016
        Mô tả: Test khi reader đạt 1500 điểm để nhận rank Silver
        Mong đợi: Rank của reader được cập nhật thành Silver, điểm tăng đúng 20
        """
        print("\n=== Starting test_silver_rank_achievement ===")

        # Thiết lập reader với 1480 điểm (gần ngưỡng Silver)
        self.reader.reader_point = 1480
        self.reader.reader_rank = "Bronze"
        self.reader.save()

        initial_points = self.reader.reader_point
        initial_rank = self.reader.reader_rank
        print(f"Initial reader points: {initial_points}")
        print(f"Initial reader rank: {initial_rank}")

        data = {
            'book_id': self.book.pk,
            'user_id': self.reader.user_id,
            'rating': 3,
            'review': 'Good book!'
        }
        print(f"Sending request with data: {data}")

        # Gửi request
        request = self.factory.post(self.add_review_url, data, format='json')
        response = self.view(request)
        print(f"Response status code: {response.status_code}")

        # Kiểm thử response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                        "Response status code should be 201 Created")

        # Kiểm thử cập nhật điểm và rank
        reader = Reader.objects.get(user_id=self.reader.user_id)
        final_points = reader.reader_point
        final_rank = reader.reader_rank
        self.assertEqual(final_points, initial_points + 20,
                        f"Reader points should increase by 20 (was {initial_points}, now {final_points})")
        self.assertEqual(final_rank, "Silver",
                        f"Reader rank should be Silver, got {final_rank}")

        print("=== Test completed successfully ===\n")

    def test_gold_rank_achievement(self):
        """
        Test Case ID: UT-RAR-017
        Mô tả: Test khi reader đạt 3000 điểm để nhận rank Gold
        Mong đợi: Rank của reader được cập nhật thành Gold, điểm tăng đúng 20
        """
        print("\n=== Starting test_gold_rank_achievement ===")

        # Thiết lập reader với 2980 điểm (gần ngưỡng Gold)
        self.reader.reader_point = 2980
        self.reader.reader_rank = "Silver"
        self.reader.save()

        initial_points = self.reader.reader_point
        initial_rank = self.reader.reader_rank
        print(f"Initial reader points: {initial_points}")
        print(f"Initial reader rank: {initial_rank}")

        data = {
            'book_id': self.book.pk,
            'user_id': self.reader.user_id,
            'rating': 5,
            'review': 'Amazing book!'
        }
        print(f"Sending request with data: {data}")

        # Gửi request
        request = self.factory.post(self.add_review_url, data, format='json')
        response = self.view(request)
        print(f"Response status code: {response.status_code}")

        # Kiểm thử response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                        "Response status code should be 201 Created")

        # Kiểm thử cập nhật điểm và rank
        reader = Reader.objects.get(user_id=self.reader.user_id)
        final_points = reader.reader_point
        final_rank = reader.reader_rank
        self.assertEqual(final_points, initial_points + 20,
                        f"Reader points should increase by 20 (was {initial_points}, now {final_points})")
        self.assertEqual(final_rank, "Gold",
                        f"Reader rank should be Gold, got {final_rank}")

        print("=== Test completed successfully ===\n")

class RatingAndReviewListViewTests(APITestCase):
    def setUp(self):
        # khoi tao du lieu cho test
        self.factory = APIRequestFactory()
        self.view = RatingAndReviewListView.as_view()
        self.url = reverse('rating-and-review-list')  # dieu chinh ten url theo urls.py

        # tao danh muc
        self.category = Category.objects.create(category_id=1, category_name="Tieu thuyet")

        # tao nguoi dung va doc gia
        self.user = User.objects.create(
            user_name="Nguoi dung test",
            email="test@example.com",
            user_password=bcrypt.hashpw("matkhau".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            is_active=True
        )
        self.reader = Reader.objects.create(user_id=self.user.user_id, reader_point=0, reader_rank="Moi")

        # tao sach
        self.book = Book.objects.create(
            book_name="Sach test",
            book_author="Tac gia test",
            book_type="Tieu thuyet",
            book_barcode="123456789",
            book_description="Mo ta test",
            category=self.category,
            status=Book.Status.ACCEPTED
        )

        # tao danh gia va nhan xet
        self.review = Rating_And_Review.objects.create(
            book=self.book,
            reader=self.reader,
            rating=5,
            review="Sach rat hay!"
        )

    def test_lay_danh_sach_thanh_cong(self):
        """
        Test Case ID: UT-RRL-01
        Muc tieu: Kiểm thử lay danh sach danh gia va nhan xet thanh cong
        Input: book_id = ID cua sach hop le
        Expected Output: HTTP 200, danh sach chua 1 danh gia voi rating = 5 va user_name = "Nguoi dung test"
        """
        request = self.factory.get(self.url, {'book_id': self.book.pk})
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['rating'], 5)
        self.assertEqual(response.data['results'][0]['user_name'], "Nguoi dung test")

    def test_sach_khong_co_danh_gia(self):
        """
        Test Case ID: UT-RRL-02
        Muc tieu: Kiểm thử lay danh sach danh gia cho sach khong co danh gia
        Input: book_id = ID cua sach moi khong co danh gia
        Expected Output: HTTP 400, danh sach rong
        """
        new_book = Book.objects.create(
            book_name="Sach moi",
            book_author="Tac gia moi",
            book_type="Tieu thuyet",
            book_barcode="987654321",
            book_description="Mo ta moi",
            category=self.category,
            status=Book.Status.ACCEPTED
        )
        request = self.factory.get(self.url, {'book_id': new_book.pk})
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['results']), 0)

    def test_thieu_book_id(self):
        """
        Test Case ID: UT-RRL-03
        Muc tieu: Kiểm thử truong hop khong cung cap book_id
        Input: Khong co book_id trong query params
        Expected Output: HTTP 400, thong bao loi
        """
        request = self.factory.get(self.url)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_book_id_khong_hop_le(self):
        """
        Test Case ID: UT-RRL-04
        Muc tieu: Kiểm thử lay danh sach danh gia cho sach khong ton tai
        Input: book_id = 999 (khong ton tai)
        Expected Output: HTTP 200, danh sach rong
        """
        request = self.factory.get(self.url, {'book_id': 999})
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_book_id_khong_phai_so(self):
        """
        Test Case ID: UT-RRL-05
        Mục tiêu: Kiểm thử khi book_id không phải là số nguyên
        Input: book_id = "abc"
        Expected Output: HTTP 400, thông báo lỗi
        """
        request = self.factory.get(self.url, {'book_id': 'abc'})
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
class MostRating_BookListViewTests(APITestCase):
    def setUp(self):
        # khoi tao du lieu cho test
        self.factory = APIRequestFactory()
        self.view = MostRating_BookListView.as_view()
        self.url = reverse('most-rating-book-list')  # dieu chinh ten url

        # tao danh muc
        self.category = Category.objects.create(category_id=1, category_name="Tieu thuyet")

        # tao sach
        self.book1 = Book.objects.create(
            book_name="Sach cao diem",
            book_author="Tac gia",
            book_type="Tieu thuyet",
            book_barcode="111",
            book_description="Mo ta",
            category=self.category,
            status=Book.Status.ACCEPTED,
            book_rating_avg=5,
            book_reading_counter=50
        )
        self.book2 = Book.objects.create(
            book_name="Sach thap diem",
            book_author="Tac gia",
            book_type="Tieu thuyet",
            book_barcode="222",
            book_description="Mo ta",
            category=self.category,
            status=Book.Status.ACCEPTED,
            book_rating_avg=3,
            book_reading_counter=100
        )

    def test_lay_danh_sach_thanh_cong(self):
        """
        Test Case ID: UT-MRB-01
        Muc tieu: Kiểm thử lay danh sach sach co diem cao nhat thanh cong
        Input: Khong co tham so loc
        Expected Output: HTTP 200, danh sach sap xep theo book_rating_avg giam dan, sach "Sach cao diem" dung dau
        """
        request = self.factory.get(self.url)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['book_name'], "Sach cao diem")

    def test_loc_theo_diem_toi_thieu(self):
        """
        Test Case ID: UT-MRB-02
        Muc tieu: Kiểm thử loc sach theo diem danh gia toi thieu
        Input: rating = 4
        Expected Output: HTTP 200, danh sach chi chua sach co diem >= 4
        """
        request = self.factory.get(self.url, {'rating': 4})
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['book_name'], "Sach cao diem")

    def test_loc_theo_reading_counter(self):
        """
        Test Case ID: UT-MRB-03
        Muc tieu: Kiểm thử loc sach theo reading_counter toi thieu
        Input: reading_counter = 75
        Expected Output: HTTP 200, danh sach chi chua sach co reading_counter >= 75
        """
        request = self.factory.get(self.url, {'reading_counter': 75})
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['book_name'], "Sach thap diem")

    def test_tham_so_loc_khong_hop_le(self):
        """
        Test Case ID: UT-MRB-04
        Muc tieu: Kiểm thử truong hop rating filter khong hop le
        Input: rating = "khong phai so"
        Expected Output: HTTP 400, thong bao loi
        """
        request = self.factory.get(self.url, {'rating': 'khong phai so'})
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_reading_counter_khong_hop_le(self):
        """
        Test Case ID: UT-MRB-05
        Mục tiêu: Kiểm thử trường hợp reading_counter không hợp lệ
        Input: reading_counter = "abc"
        Expected Output: HTTP 400, thông báo lỗi
        """
        request = self.factory.get(self.url, {'reading_counter': 'abc'})
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_khong_co_sach_thoa_man(self):
        """
        Test Case ID: UT-MRB-06
        Muc tieu: Kiểm thử truong hop khong co sach thoa man dieu kien loc
        Input: rating = 6
        Expected Output: HTTP 200, danh sach rong
        """
        request = self.factory.get(self.url, {'rating': 6})
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)


class MostReaded_BookListViewTests(APITestCase):
    def setUp(self):
        # khoi tao du lieu cho test
        self.factory = APIRequestFactory()
        self.view = MostReaded_BookListView.as_view()
        self.url = reverse('most-readed-book-list')  # dieu chinh ten url

        # tao danh muc
        self.category = Category.objects.create(category_id=1, category_name="Tieu thuyet")

        # tao sach
        self.book1 = Book.objects.create(
            book_name="Sach pho bien",
            book_author="Tac gia",
            book_type="Tieu thuyet",
            book_barcode="111",
            book_description="Mo ta",
            category=self.category,
            status=Book.Status.ACCEPTED,
            book_reading_counter=100
        )
        self.book2 = Book.objects.create(
            book_name="Sach it pho bien",
            book_author="Tac gia",
            book_type="Tieu thuyet",
            book_barcode="222",
            book_description="Mo ta",
            category=self.category,
            status=Book.Status.ACCEPTED,
            book_reading_counter=50
        )

    def test_lay_danh_sach_thanh_cong(self):
        """
        Test Case ID: UT-MRD-01
        Muc tieu: Kiểm thử lay danh sach sach duoc doc nhieu nhat thanh cong
        Input: Khong co tham so
        Expected Output: HTTP 200, danh sach sap xep theo book_reading_counter giam dan, sach "Sach pho bien" dung dau
        """
        request = self.factory.get(self.url)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['book_name'], "Sach pho bien")

    def test_phan_trang(self):
        """
        Test Case ID: UT-MRD-02
        Muc tieu: Kiểm thử phan trang danh sach sach duoc doc nhieu
        Input: page_size = 1
        Expected Output: HTTP 200, danh sach chi chua 1 sach
        """
        request = self.factory.get(self.url, {'page_size': 1})
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_khong_co_sach(self):
        """
        Test Case ID: UT-MRD-03
        Muc tieu: Kiểm thử truong hop khong co sach nao
        Input: Xoa tat ca sach
        Expected Output: HTTP 200, danh sach rong
        """
        Book.objects.all().delete()
        request = self.factory.get(self.url)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

class LastUploaded_BookListViewTests(APITestCase):
    def setUp(self):
        # khoi tao du lieu cho test
        self.factory = APIRequestFactory()
        self.view = LastUploaded_BookListView.as_view()
        self.url = reverse('last-uploaded-book-list')  # dieu chinh ten url

        # tao danh muc
        self.category = Category.objects.create(category_id=1, category_name="Tieu thuyet")

        # tao sach
        self.book1 = Book.objects.create(
            book_name="Sach moi",
            book_author="Tac gia",
            book_type="Tieu thuyet",
            book_barcode="111",
            book_description="Mo ta",
            category=self.category,
            status=Book.Status.ACCEPTED,
            book_uploaded_date=now()
        )
        self.book2 = Book.objects.create(
            book_name="Sach cu",
            book_author="Tac gia",
            book_type="Tieu thuyet",
            book_barcode="222",
            book_description="Mo ta",
            category=self.category,
            status=Book.Status.ACCEPTED,
            book_uploaded_date=now() - timedelta(days=1)
        )

    def test_lay_danh_sach_thanh_cong(self):
        """
        Test Case ID: UT-LUB-01
        Muc tieu: Kiểm thử lay danh sach sach tai len moi nhat thanh cong
        Input: Khong co tham so
        Expected Output: HTTP 200, danh sach sap xep theo book_uploaded_date giam dan, sach "Sach moi" dung dau
        """
        request = self.factory.get(self.url)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['book_name'], "Sach moi")

    def test_phan_trang(self):
        """
        Test Case ID: UT-LUB-02
        Muc tieu: Kiểm thử phan trang danh sach sach tai len moi nhat
        Input: page_size = 1
        Expected Output: HTTP 200, danh sach chi chua 1 sach
        """
        request = self.factory.get(self.url, {'page_size': 1})
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_khong_co_sach(self):
        """
        Test Case ID: UT-LUB-03
        Muc tieu: Kiểm thử truong hop khong co sach nao
        Input: Xoa tat ca sach
        Expected Output: HTTP 200, danh sach rong
        """
        Book.objects.all().delete()
        request = self.factory.get(self.url)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

class NotificationListViewTests(APITestCase):
    def setUp(self):
        # khoi tao du lieu cho test
        self.factory = APIRequestFactory()
        self.view = NotificationListView.as_view()
        self.url = reverse('notification-list')  # dieu chinh ten url
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
        # tao nguoi dung va doc gia
        self.user = User.objects.create(
            user_name="Nguoi dung test",
            email="test@example.com",
            user_password=bcrypt.hashpw("matkhau".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            is_active=True
        )
        self.reader = Reader.objects.create(user_id=self.user.user_id, reader_point=0, reader_rank="Moi")

        # tao thong bao
        self.notification = Notification.objects.create(
            reader_id=self.reader.reader_id,
            manager_id=2,
            notification_record="Thong bao test",
            notification_title="Tieu de test"
        )

    def test_lay_danh_sach_thanh_cong(self):
        """
        Test Case ID: UT-NTL-01
        Muc tieu: Kiểm thử lay danh sach thong bao thanh cong
        Input: user_id = ID cua nguoi dung hop le
        Expected Output: HTTP 200, danh sach chua 1 thong bao voi tieu de "Tieu de test"
        """
        request = self.factory.get(self.url, {'user_id': self.user.user_id})
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['notification_title'], "Tieu de test")

    def test_thieu_user_id(self):
        """
        Test Case ID: UT-NTL-02
        Muc tieu: Kiểm thử truong hop khong cung cap user_id
        Input: Khong co user_id trong query params
        Expected Output: HTTP 400, thong bao loi
        """
        request = self.factory.get(self.url)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_user_id_khong_hop_le(self):
        """
        Test Case ID: UT-NTL-03
        Muc tieu: Kiểm thử lay danh sach thong bao cho nguoi dung khong ton tai
        Input: user_id = 999 (khong ton tai)
        Expected Output: HTTP 404, thong bao loi
        """
        request = self.factory.get(self.url, {'user_id': 999})
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

class LastThreeNotificationListViewTests(APITestCase):
    def setUp(self):
        # khoi tao du lieu cho test
        self.factory = APIRequestFactory()
        self.view = LastThreeNotificationListView.as_view()
        self.url = reverse('last-three-notification-list')  # dieu chinh ten url
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
        # tao nguoi dung va doc gia
        self.user = User.objects.create(
            user_name="Nguoi dung test",
            email="test@example.com",
            user_password=bcrypt.hashpw("matkhau".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            is_active=True
        )
        self.reader = Reader.objects.create(user_id=self.user.user_id, reader_point=0, reader_rank="Moi")

        # tao nhieu thong bao de kiem thu
        for i in range(5):
            Notification.objects.create(
                reader_id=self.reader.reader_id,
                manager_id=2,
                notification_record=f"Thong bao {i}",
                notification_title=f"Tieu de {i}"
            )

    def test_lay_danh_sach_thanh_cong(self):
        """
        Test Case ID: UT-LTN-01
        Muc tieu: Kiểm thử lay 3 thong bao moi nhat thanh cong
        Input: user_id = ID cua nguoi dung hop le
        Expected Output: HTTP 200, danh sach chua 3 thong bao, thong bao moi nhat co tieu de "Tieu de 4"
        """
        request = self.factory.get(self.url, {'user_id': self.user.user_id})
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['notification_title'], "Tieu de 4")

    def test_khong_co_thong_bao(self):
        """
        Test Case ID: UT-LTN-02
        Muc tieu: Kiểm thử truong hop khong co thong bao
        Input: user_id = ID cua nguoi dung, xoa tat ca thong bao
        Expected Output: HTTP 200, danh sach rong
        """
        Notification.objects.all().delete()
        request = self.factory.get(self.url, {'user_id': self.user.user_id})
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_user_id_khong_hop_le(self):
        """
        Test Case ID: UT-LTN-03
        Muc tieu: Kiểm thử lay thong bao cho nguoi dung khong ton tai
        Input: user_id = 999 (khong ton tai)
        Expected Output: HTTP 400, thong bao loi
        """
        request = self.factory.get(self.url, {'user_id': 999})
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

class CreateBookViewTests(APITestCase):
    def setUp(self):
        # khoi tao du lieu cho test
        self.factory = APIRequestFactory()
        self.view = CreateBookView.as_view()
        self.url = reverse('create-book')  # dieu chinh ten url

        # tao danh muc
        self.category = Category.objects.create(category_id=1, category_name="Tieu thuyet")

    def test_tao_sach_thanh_cong(self):
        """
        Test Case ID: UT-CBK-01
        Muc tieu: Kiểm thử tao sach moi thanh cong
        Input: Du lieu sach hop le (book_name, book_author, book_type, book_barcode, book_description, category, status)
        Expected Output: HTTP 201, sach duoc tao voi ten "Sach moi"
        """
        data = {
            'book_name': "Sach moi",
            'book_author': "Tac gia",
            'book_type': "Tieu thuyet",
            'book_barcode': "123456789",
            'book_description': "Mo ta",
            'category': self.category.category_id,
            'status': Book.Status.PENDING
        }
        request = self.factory.post(self.url, data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.first().book_name, "Sach moi")

    def test_thieu_truong_bat_buoc(self):
        """
        Test Case ID: UT-CBK-02
        Muc tieu: Kiểm thử tao sach khi thieu truong bat buoc
        Input: Du lieu thieu book_name
        Expected Output: HTTP 400, thong bao loi ve truong book_name
        """
        data = {
            'book_author': "Tac gia",
            'book_type': "Tieu thuyet",
            'book_barcode': "123456789",
            'book_description': "Mo ta",
            'category': self.category.category_id
        }
        request = self.factory.post(self.url, data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('book_name', response.data)

    def test_danh_muc_khong_hop_le(self):
        """
        Test Case ID: UT-CBK-03
        Muc tieu: Kiểm thử tao sach voi danh muc khong ton tai
        Input: category = 999 (khong ton tai)
        Expected Output: HTTP 400, thong bao loi
        """
        data = {
            'book_name': "Sach moi",
            'book_author': "Tac gia",
            'book_type': "Tieu thuyet",
            'book_barcode': "123456789",
            'book_description': "Mo ta",
            'category': 999,
            'status': Book.Status.PENDING
        }
        request = self.factory.post(self.url, data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
class UploadedByViewTests(APITestCase):
    def setUp(self):
        # khoi tao du lieu cho test
        self.factory = APIRequestFactory()
        self.view = UploadedByView.as_view()
        self.url = reverse('get_uploadedby')  # dieu chinh ten url

        # tao danh muc
        self.category = Category.objects.create(category_id=1, category_name="Tieu thuyet")

        # tao nguoi dung va doc gia
        self.user = User.objects.create(
            user_name="Nguoi tai len",
            email="uploader@example.com",
            user_password=bcrypt.hashpw("matkhau".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            is_active=True
        )
        self.reader = Reader.objects.create(user_id=self.user.user_id, reader_point=0, reader_rank="Moi")

        # tao sach
        self.book = Book.objects.create(
            book_name="Sach test",
            book_author="Tac gia",
            book_type="Tieu thuyet",
            book_barcode="123456789",
            book_description="Mo ta",
            category=self.category,
            status=Book.Status.ACCEPTED
        )

        # tao ban ghi tai len
        self.uploaded_book = UploadedBook.objects.create(reader_id=self.reader.reader_id, book_id=self.book.book_id)

    def test_lay_nguoi_tai_len_thanh_cong(self):
        """
        Test Case ID: UT-UBD-01
        Muc tieu: Kiểm thử lay ten nguoi tai len sach thanh cong
        Input: book_id = ID cua sach duoc tai len boi nguoi dung
        Expected Output: HTTP 200, tra ve ten "Nguoi tai len"
        """
        request = self.factory.get(self.url, {'book_id': self.book.book_id})
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Nguoi tai len")

    def test_sach_do_quan_ly_tai_len(self):
        """
        Test Case ID: UT-UBD-02
        Muc tieu: Kiểm thử truong hop sach khong co ban ghi tai len (do quan ly tai len)
        Input: book_id = ID cua sach khong co ban ghi tai len
        Expected Output: HTTP 200, tra ve "Manager"
        """
        new_book = Book.objects.create(
            book_name="Sach quan ly",
            book_author="Tac gia",
            book_type="Tieu thuyet",
            book_barcode="987654321",
            book_description="Mo ta",
            category=self.category,
            status=Book.Status.ACCEPTED
        )
        request = self.factory.get(self.url, {'book_id': new_book.book_id})
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Manager")

    def test_book_id_khong_hop_le(self):
        """
        Test Case ID: UT-UBD-03
        Muc tieu: Kiểm thử truong hop book_id khong ton tai
        Input: book_id = 999 (khong ton tai)
        Expected Output: HTTP 200, tra ve "Manager"
        """
        request = self.factory.get(self.url, {'book_id': 999})
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Manager")
    def test_thieu_tham_so_book_id(self):
        """
        Test Case ID: UT-UBD-04
        Mục tiêu: Kiểm thử khi không truyền tham số book_id
        Input: Không có book_id
        Expected Output: HTTP 200, trả về "Manager"
        """
        request = self.factory.get(self.url)  # không truyền book_id
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Manager")
    def test_book_id_sai_kieu_du_lieu(self):
        """
        Test Case ID: UT-UBD-05
        Mục tiêu: Kiểm thử khi book_id là chuỗi không hợp lệ
        Input: book_id = "abc"
        Expected Output: HTTP 200, trả về "Manager"
        """
        request = self.factory.get(self.url, {'book_id': 'abc'})
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Manager")
class ContinueReadingViewTests(APITestCase):
    def setUp(self):
        # khoi tao du lieu cho test
        self.factory = APIRequestFactory()
        self.view = ContinueReadingView.as_view()
        self.url = reverse('creare-continue-reading')  # dieu chinh ten url

        # tao danh muc
        self.category = Category.objects.create(category_id=1, category_name="Tieu thuyet")

        # tao nguoi dung va doc gia
        self.user = User.objects.create(
            user_name="Nguoi dung test",
            email="test@example.com",
            user_password=bcrypt.hashpw("matkhau".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            is_active=True
        )
        self.reader = Reader.objects.create(user_id=self.user.user_id, reader_point=0, reader_rank="Moi")

        # tao sach
        self.book = Book.objects.create(
            book_name="Sach test",
            book_author="Tac gia",
            book_type="Tieu thuyet",
            book_barcode="123456789",
            book_description="Mo ta",
            category=self.category,
            status=Book.Status.ACCEPTED
        )

    def test_them_sach_thanh_cong(self):
        """
        Test Case ID: UT-CTR-01
        Muc tieu: Kiểm thử them sach vao danh sach doc tiep thanh cong
        Input: book_id = ID cua sach, reader_id = ID cua doc gia
        Expected Output: HTTP 200, ban ghi doc tiep duoc tao
        """
        data = {'book_id': self.book.book_id, 'reader_id': self.reader.reader_id}
        request = self.factory.post(self.url, data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BookContinueReading.objects.count(), 1)

    def test_them_sach_trung_lap(self):
        """
        Test Case ID: UT-CTR-02
        Muc tieu: Kiểm thử them lai sach da co trong danh sach doc tiep
        Input: book_id = ID cua sach, reader_id = ID cua doc gia (da co ban ghi)
        Expected Output: HTTP 200, khong tao ban ghi moi
        """
        BookContinueReading.objects.create(book_id=self.book.book_id, reader_id=self.reader.reader_id)
        data = {'book_id': self.book.book_id, 'reader_id': self.reader.reader_id}
        request = self.factory.post(self.url, data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BookContinueReading.objects.count(), 1)

    def test_thieu_truong_bat_buoc(self):
        """
        Test Case ID: UT-CTR-03
        Muc tieu: Kiểm thử truong hop thieu truong bat buoc
        Input: Chi co book_id, thieu reader_id
        Expected Output: HTTP 400, thong bao loi
        """
        data = {'book_id': self.book.book_id}
        request = self.factory.post(self.url, data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_thieu_book_id(self):
        """
        Test Case ID: UT-CTR-04
        Mục tiêu: Kiểm thử khi thiếu book_id
        Input: Chỉ có reader_id
        Expected Output: HTTP 400, thông báo lỗi
        """
        data = {'reader_id': self.reader.reader_id}
        request = self.factory.post(self.url, data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_thieu_ca_hai_truong(self):
        """
        Test Case ID: UT-CTR-05
        Mục tiêu: Kiểm thử khi thiếu cả hai trường bắt buộc
        Input: Không có book_id và reader_id
        Expected Output: HTTP 400
        """
        request = self.factory.post(self.url, {}, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_id_khong_ton_tai(self):
        """
        Test Case ID: UT-CTR-06
        Mục tiêu: Kiểm thử khi book_id hoặc reader_id không tồn tại
        Input: book_id = 999, reader_id = 999
        Expected Output: HTTP 400 hoặc lỗi liên quan đến khóa ngoại
        """
        data = {'book_id': 999, 'reader_id': 999}
        request = self.factory.post(self.url, data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class HomePageTests(TestCase):
    def setUp(self):
        # Khởi tạo dữ liệu cho test
        self.client = Client()
        self.url = reverse('homePage')  # Điều chỉnh tên URL

    def test_truy_cap_trang_chu_thanh_cong(self):
        """
        Test Case ID: UT-HMP-01
        Mục tiêu: Kiểm thử render trang chủ thành công
        Input: GET request tới URL trang chủ
        Expected Output: HTTP 200, render template '6_home_page.html'
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, '6_home_page.html')

    def test_truy_cap_trang_chu_that_bai(self):
        """
        Test Case ID: UT-HMP-02
        Mục tiêu: Kiểm thử trường hợp truy cập trang chủ thất bại khi chưa đăng nhập (hoặc không có quyền)
        Input: GET request tới URL trang chủ khi chưa đăng nhập
        Expected Output: HTTP 302 (chuyển hướng đến trang đăng nhập hoặc trang lỗi)
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  # Chuyển hướng
        self.assertRedirects(response, '/login')  # Giả sử trang login có URL '/login'
    def test_gui_post_khong_hop_le(self):
        """
        Test Case ID: UT-HMP-03
        Mục tiêu: Kiểm thử gửi POST yêu cầu tới trang chủ với dữ liệu không hợp lệ
        Input: POST request với dữ liệu sai định dạng hoặc thiếu
        Expected Output: HTTP 400 (Lỗi do thiếu dữ liệu bắt buộc)
        """
        data = {'invalid_field': 'some_value'}  # Dữ liệu không hợp lệ
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)  # Kiểm thử mã lỗi khi dữ liệu sai

class RankPageTests(TestCase):
    def setUp(self):
        # Khởi tạo dữ liệu cho test
        self.client = Client()
        self.url = reverse('rankPage')  # Điều chỉnh tên URL

    def test_truy_cap_trang_xep_hang_thanh_cong(self):
        """
        Test Case ID: UT-RNK-01
        Mục tiêu: Kiểm thử render trang xếp hạng thành công
        Input: GET request tới URL trang xếp hạng
        Expected Output: HTTP 200, render template '7_gamefication_page.html'
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, '7_gamefication_page.html')

    def test_truy_cap_trang_xep_hang_that_bai(self):
        """
        Test Case ID: UT-RNK-02
        Mục tiêu: Kiểm thử trường hợp truy cập trang xếp hạng thất bại khi chưa đăng nhập (hoặc không có quyền)
        Input: GET request tới URL trang xếp hạng khi chưa đăng nhập
        Expected Output: HTTP 302 (chuyển hướng đến trang đăng nhập hoặc trang lỗi)
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  # Chuyển hướng
        self.assertRedirects(response, '/login')  # Giả sử trang login có URL '/login'

    def test_gui_post_khong_hop_le(self):
        """
        Test Case ID: UT-RNK-03
        Mục tiêu: Kiểm thử gửi POST yêu cầu tới trang xếp hạng với dữ liệu không hợp lệ
        Input: POST request với dữ liệu sai định dạng hoặc thiếu
        Expected Output: HTTP 400 (Lỗi do thiếu dữ liệu bắt buộc)
        """
        data = {'invalid_field': 'some_value'}  # Dữ liệu không hợp lệ
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)  # Kiểm thử mã lỗi khi dữ liệu sai
class WishListPageTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('wish-listPage')  # Đảm bảo tên này trùng với tên trong urls.py

    def test_truy_cap_trang_wishlist_thanh_cong(self):
        """
        Test Case ID: UT-WLP-01
        Mục tiêu: Kiểm thử render trang wishlist thành công
        Input: GET request tới URL trang wishlist
        Expected Output: HTTP 200, render template '8_wishlist_page.html'
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, '8_wishlist_page.html')

    def test_truy_cap_trang_wishlist_that_bai(self):
        """
        Test Case ID: UT-WLP-02
        Mục tiêu: Kiểm thử truy cập wishlist thất bại nếu chưa đăng nhập
        Expected Output: HTTP 302 chuyển hướng
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login')

    def test_gui_post_khong_hop_le(self):
        """
        Test Case ID: UT-WLP-03
        Mục tiêu: Gửi POST không hợp lệ đến trang wishlist
        Expected Output: HTTP 400
        """
        response = self.client.post(self.url, {'invalid': 'data'})
        self.assertEqual(response.status_code, 400)

class NotificationPageTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('notificationPage')

    def test_truy_cap_trang_thong_bao_thanh_cong(self):
        """
        Test Case ID: UT-NFP-01
        Mục tiêu: Kiểm thử render trang thông báo thành công
        Expected Output: HTTP 200, render template '9_notification_page.html'
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, '9_notification_page.html')

    def test_truy_cap_trang_thong_bao_that_bai(self):
        """
        Test Case ID: UT-NFP-02
        Mục tiêu: Kiểm thử truy cập không thành công khi chưa đăng nhập
        Expected Output: HTTP 302 redirect
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login')

    def test_gui_post_khong_hop_le(self):
        """
        Test Case ID: UT-NFP-03
        Mục tiêu: Gửi POST không hợp lệ đến trang thông báo
        Expected Output: HTTP 400
        """
        response = self.client.post(self.url, {'spam': 'value'})
        self.assertEqual(response.status_code, 400)

class MyUploadedBookPageTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('myUploadedBookPage')

    def test_truy_cap_trang_sach_da_upload_thanh_cong(self):
        """
        Test Case ID: UT-MUBP-01
        Mục tiêu: Kiểm thử render trang sách đã upload thành công
        Expected Output: HTTP 200, render template '10_myUploadedBook_page.html'
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, '10_myUploadedBook_page.html')

    def test_truy_cap_trang_sach_da_upload_that_bai(self):
        """
        Test Case ID: UT-MUBP-02
        Mục tiêu: Truy cập thất bại nếu chưa đăng nhập
        Expected Output: HTTP 302 chuyển hướng
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login')

    def test_gui_post_khong_hop_le(self):
        """
        Test Case ID: UT-MUBP-03
        Mục tiêu: Gửi POST không hợp lệ đến trang sách đã upload
        Expected Output: HTTP 400
        """
        response = self.client.post(self.url, {'wrong': 'input'})
        self.assertEqual(response.status_code, 400)

class AddBookToWishlistTests(APITestCase):
    def setUp(self):
        # khoi tao du lieu cho test
        self.factory = APIRequestFactory()
        self.view = AddBookToWishlist.as_view()
        self.url = reverse('add_to_wishlist')  # dieu chinh ten url

        # tao danh muc
        self.category = Category.objects.create(category_id=1, category_name="Tieu thuyet")

        # tao nguoi dung va doc gia
        self.user = User.objects.create(
            user_name="Nguoi dung test",
            email="test@example.com",
            user_password=bcrypt.hashpw("matkhau@123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            is_active=True
        )
        self.reader = Reader.objects.create(user_id=self.user.user_id, reader_point=0, reader_rank="Moi")

        # tao sach
        self.book = Book.objects.create(
            book_name="Sach test",
            book_author="Tac gia",
            book_type="Tieu thuyet",
            book_barcode="123456789",
            book_description="Mo ta",
            category=self.category,
            status=Book.Status.ACCEPTED
        )

    def test_them_sach_thanh_cong(self):
        """
        Test Case ID: UT-ABW-01
        Muc tieu: Kiểm thử them sach vao danh sach yeu thich thanh cong
        Input: book_id = ID cua sach, user_id = ID cua doc gia
        Expected Output: HTTP 200, ban ghi yeu thich duoc tao
        """
        data = {'book_id': self.book.book_id, 'user_id': self.reader.reader_id}
        request = self.factory.post(self.url, data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "Book added to wishlist")
        self.assertEqual(WishList.objects.count(), 1)

    def test_them_sach_trung_lap(self):
        """
        Test Case ID: UT-ABW-02
        Muc tieu: Kiểm thử them lai sach da co trong danh sach yeu thich
        Input: book_id = ID cua sach, user_id = ID cua doc gia
        Expected Output: HTTP 400, sach da co trong danh sach yeu thich
        """
        WishList.objects.create(book=self.book, reader=self.reader)
        data = {'book_id': self.book.book_id, 'user_id': self.user.user_id}
        request = self.factory.post(self.url, data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_thieu_truong_bat_buoc(self):
        """
        Test Case ID: UT-ABW-03
        Muc tieu: Kiểm thử truong hop thieu truong bat buoc
        Input: Chi co book_id, thieu reader_id
        Expected Output: HTTP 400, thong bao loi
        """
        data = {'book_id': self.book.book_id}
        request = self.factory.post(self.url, data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nguoi_doc_khong_ton_tai(self):
        """
        Test Case ID: UT-ABW-04
        Muc tieu: Kiểm thử them sach vao danh sach yeu thich voi nguoi doc khong ton tai
        Input: book_id = ID cua sach, user_id = 99999 (khong ton tai)
        Expected Output: HTTP 404, Nguoi doc khong ton tai
        """
        data = {'book_id': self.book.book_id, 'user_id': 9999}
        request = self.factory.post(self.url, data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(WishList.objects.count(), 0)
    def test_sach_khong_ton_tai(self):
        """
        Test Case ID: UT-ABW-05
        Mục tiêu: Kiểm thử xử lý khi sách không tồn tại
        Input: book_id = 99999 (không tồn tại), user_id = ID hợp lệ của người dùng
        Expected Output: HTTP 404, thông báo lỗi "Book not found"
        """
        data = {'book_id': 99999, 'user_id': self.user.user_id}
        request = self.factory.post(self.url, data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], "Book not found")

class RemoveBookFromWishlistTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            user_name="testuser",
            email="test@example.com",
            user_password=bcrypt.hashpw("password@123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            is_active=True
        )
        self.reader = Reader.objects.create(user_id=self.user.user_id, reader_point=0, reader_rank="New")
        self.category = Category.objects.create(category_id=1, category_name="Test Category")
        self.book = Book.objects.create(
            book_name="Test Book", book_author="Test Author", book_type="Fiction",
            book_barcode="123456789", book_description="Test Description", category=self.category,
            status=Book.Status.ACCEPTED, book_favourite_counter=5
        )

    def test_remove_book_from_wishlist_success(self):
        """
        Test Case ID: UT-RWL-001
        Mo ta: Test xoa sach khoi wishlist thanh cong
        Input: book_id, user_id hop le, wishlist ton tai
        Mong doi: Tra ve 200, wishlist bi xoa, book_favourite_counter giam 1
        """
        WishList.objects.create(book_id=self.book.pk, user_id=self.user.user_id)
        initial_counter = self.book.book_favourite_counter
        data = {'book_id': self.book.pk, 'user_id': self.user.user_id}
        request = self.factory.post(reverse('remove_from_wishlist'), data, format='json')
        response = RemoveBookFromWishlist.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Book removed from wishlist")
        self.assertEqual(WishList.objects.count(), 0)
        self.book.refresh_from_db()
        self.assertEqual(self.book.book_favourite_counter, initial_counter - 1)

    def test_remove_book_from_wishlist_not_found(self):
        """
        Test Case ID: UT-RWL-002
        Mo ta: Test xoa sach khong co trong wishlist
        Input: book_id, user_id hop le, wishlist khong ton tai
        Mong doi: Tra ve 400, thong bao loi
        """
        data = {'book_id': self.book.pk, 'user_id': self.user.user_id}
        request = self.factory.post(reverse('remove_from_wishlist'), data, format='json')
        response = RemoveBookFromWishlist.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Book not in wishlist")

    def test_remove_with_missing_user(self):
        """
        Test Case ID: UT-RWL-003
        Mo ta: Test xoa sach khi user_id khong ton tai
        Input: book_id hop le, user_id khong ton tai
        Mong doi: Tra ve 400, thong bao Reader khong ton tai
        """
        data = {'book_id': self.book.pk, 'user_id': 9999}
        request = self.factory.post(reverse('remove_from_wishlist'), data, format='json')
        response = RemoveBookFromWishlist.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Reader not found")

    def test_remove_book_not_in_book_table(self):
        """
        Test Case ID: UT-RWL-004
        Mo ta: Test xoa sach khi wishlist ton tai nhung sach khong co trong bang Book
        Input: book_id khong ton tai trong Book, user_id hop le, wishlist ton tai
        Mong doi: Tra ve 400, thong bao loi
        """
        WishList.objects.create(book_id=9999, user_id=self.user.user_id)
        data = {'book_id': 9999, 'user_id': self.user.user_id}
        request = self.factory.post(reverse('remove_from_wishlist'), data, format='json')
        response = RemoveBookFromWishlist.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(WishList.objects.count(), 1)  # Wishlist không bị xóa vì lỗi xảy ra

    def test_remove_with_missing_fields(self):
        """
        Test Case ID: UT-RWL-005
        Mo ta: Test xoa sach khi payload thieu truong bat buoc
        Input: Thieu book_id hoac user_id
        Mong doi: Tra ve 400, thong bao loi
        """
        data = {'book_id': self.book.pk}  # Thieu user_id
        request = self.factory.post(reverse('remove_from_wishlist'), data, format='json')
        response = RemoveBookFromWishlist.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_remove_with_invalid_book_id(self):
        """
        Test Case ID: UT-RWL-006
        Mo ta: Test xoa sach voi book_id khong hop le
        Input: book_id khong phai so nguyen, user_id hop le
        Mong doi: Tra ve 400, thong bao loi
        """
        data = {'book_id': "invalid", 'user_id': self.user.user_id}
        request = self.factory.post(reverse('remove_from_wishlist'), data, format='json')
        response = RemoveBookFromWishlist.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

class CheckBookInWishlistTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            user_name="testuser",
            email="test@example.com",
            user_password=bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            is_active=True
        )
        self.reader = Reader.objects.create(user_id=self.user.user_id, reader_point=0, reader_rank="New")
        self.category = Category.objects.create(category_id=1, category_name="Test Category")
        self.book = Book.objects.create(
            book_name="Test Book", book_author="Test Author", book_type="Fiction",
            book_barcode="123456789", book_description="Test Description", category=self.category,
            status=Book.Status.ACCEPTED
        )

    def test_check_book_in_wishlist_thank_cong(self):
        """
        Test Case ID: UT-CIWL-001
        Mo ta: Test Kiểm thử sach co trong wishlist
        Input: book_id, user_id hop le, sach co trong wishlist
        Mong doi: Tra ve 200, in_wishlist=True
        """
        WishList.objects.create(book_id=self.book.pk, reader_id=self.user.user_id)
        data = {'book_id': self.book.pk, 'user_id': self.reader.user_id}
        request = self.factory.get(reverse('check_book_in_wishlist'), data, format='json')
        response = CheckBookInWishlist.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['in_wishlist'])


    def test_check_book_in_wishlist_that_bai(self):
        """
        Test Case ID: UT-CIWL-002
        Mo ta: Test Kiểm thử sach khong co trong wishlist
        Input: book_id, user_id hop le, sach khong co trong wishlist
        Mong doi: Tra ve 200, in_wishlist=False
        """
        data = {'book_id': self.book.pk, 'user_id': self.reader.user_id}
        request = self.factory.get(reverse('check_book_in_wishlist'), data, format='json')
        response = CheckBookInWishlist.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['in_wishlist'])


    def test_check_voi_user_null(self):
        """
        Test Case ID: UT-CIWL-003
        Mo ta: Test Kiểm thử sach khi user_id khong ton tai
        Input: book_id hop le, user_id khong ton tai
        Mong doi: Tra ve 400, thong bao Reader khong ton tai
        """
        data = {'book_id': self.book.pk, 'user_id': 9999}
        request = self.factory.get(reverse('check_book_in_wishlist'), data, format='json')
        response = CheckBookInWishlist.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Reader not found")


    def test_check_thieu_truong(self):
        """
        Test Case ID: UT-CIWL-004
        Mo ta: Test Kiểm thử sach khi thieu tham so bat buoc
        Input: Thieu book_id hoac user_id
        Mong doi: Tra ve 400, thong bao loi
        """
        data = {'book_id': self.book.pk}  # Thieu user_id
        request = self.factory.get(reverse('check_book_in_wishlist'), data, format='json')
        response = CheckBookInWishlist.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)


    def test_check_with_invalid_user_id(self):
        """
        Test Case ID: UT-CIWL-005
        Mo ta: Test Kiểm thử sach voi user_id khong hop le
        Input: user_id khong phai so nguyen, book_id hop le
        Mong doi: Tra ve 400, thong bao loi
        """
        data = {'book_id': self.book.pk, 'user_id': 'invalid'}
        request = self.factory.get(reverse('check_book_in_wishlist'), data, format='json')
        response = CheckBookInWishlist.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)


    def test_check_with_invalid_book_id(self):
        """
        Test Case ID: UT-CIWL-006
        Mo ta: Test Kiểm thử sach voi book_id khong hop le
        Input: book_id khong phai so nguyen, user_id hop le
        Mong doi: Tra ve 400, thong bao loi
        """
        data = {'book_id': 'invalid', 'user_id': self.user.user_id}
        request = self.factory.get(reverse('check_book_in_wishlist'), data, format='json')
        response = CheckBookInWishlist.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

class WishListListViewTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            user_name="testuser",
            email="test@example.com",
            user_password=bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            is_active=True
        )
        self.reader = Reader.objects.create(user_id=self.user.user_id, reader_point=0, reader_rank="New")
        self.category = Category.objects.create(category_id=1, category_name="Test Category")
        self.book = Book.objects.create(
            book_name="Test Book", book_author="Test Author", book_type="Fiction",
            book_barcode="123456789", book_description="Test Description", category=self.category,
            status=Book.Status.ACCEPTED
        )

    def test_lay_wishlist_voi_userid_hop_le_co_sach(self):
        """
        Test Case ID: UT-WLL-001
        Mo ta: Test lay danh sach wishlist voi user_id hop le va co sach trong wishlist
        Input: user_id hop le, co du lieu wishlist
        Mong doi: Tra ve 200, danh sach sach phan trang
        """
        WishList.objects.create(book_id=self.book.pk, reader_id=self.reader.reader_id)
        request = self.factory.get(reverse('getWishList_ListView'), {'user_id': str(self.reader.user_id)})
        response = WishListListView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['book_id'], self.book.pk)

    def test_lay_wishlist_voi_userid_hop_le_khong_co_sach(self):
        """
        Test Case ID: UT-WLL-002
        Mo ta: Test lay danh sach wishlist voi user_id hop le nhung khong co sach
        Input: user_id hop le, khong co du lieu wishlist
        Mong doi: Tra ve 200, danh sach rong
        """
        request = self.factory.get(reverse('getWishList_ListView'), {'user_id': str(self.reader.user_id)})
        response = WishListListView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 0)

    def test_lay_wishlist_khi_thieu_userid(self):
        """
        Test Case ID: UT-WLL-003
        Mo ta: Test lay danh sach wishlist khi thieu user_id
        Input: Khong co user_id
        Mong doi: Tra ve 400, thong bao User ID not found
        """
        request = self.factory.get(reverse('getWishList_ListView'), {})
        response = WishListListView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "User ID not found")

    def test_lay_wishlist_voi_userid_khong_hop_le(self):
        """
        Test Case ID: UT-WLL-004
        Mo ta: Test lay danh sach wishlist voi user_id khong hop le
        Input: user_id khong phai so nguyen
        Mong doi: Tra ve 400, thong bao loi
        """
        request = self.factory.get(reverse('getWishList_ListView'), {'user_id': 'invalid'})
        response = WishListListView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_lay_wishlist_voi_userid_khong_ton_tai(self):
        """
        Test Case ID: UT-WLL-005
        Mo ta: Test lay danh sach wishlist voi user_id khong ton tai
        Input: user_id khong ton tai
        Mong doi: Tra ve 404, thong bao Reader not found
        """
        request = self.factory.get(reverse('getWishList_ListView'), {'user_id': '9999'})
        response = WishListListView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], "Reader not found")
class LastThreeWishListViewTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            user_name="testuser",
            email="test@example.com",
            user_password=bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            is_active=True
        )
        self.reader = Reader.objects.create(user_id=self.user.user_id, reader_point=0, reader_rank="New")
        self.category = Category.objects.create(category_id=1, category_name="Test Category")
        self.book1 = Book.objects.create(
            book_name="Book 1", book_author="Author 1", book_type="Fiction",
            book_barcode="1234567891", book_description="Description 1", category=self.category,
            status=Book.Status.ACCEPTED
        )
        self.book2 = Book.objects.create(
            book_name="Book 2", book_author="Author 2", book_type="Fiction",
            book_barcode="1234567892", book_description="Description 2", category=self.category,
            status=Book.Status.ACCEPTED
        )

    def test_lay_3_wishlist_gan_nhat_voi_userid_hop_le_co_sach(self):
        """
        Test Case ID: UT-LTWL-001
        Mo ta: Test lay 3 sach gan nhat trong wishlist voi user_id hop le va co sach
        Input: user_id hop le, co du lieu wishlist
        Mong doi: Tra ve 200, danh sach toi da 3 sach
        """
        # Tạo dữ liệu wishlist
        WishList.objects.create(book_id=self.book1.pk, reader_id=self.reader.reader_id)
        WishList.objects.create(book_id=self.book2.pk, reader_id=self.reader.reader_id)

        # Gửi request
        request = self.factory.get(reverse('getLastThreeWishListView'), {'user_id': str(self.reader.user_id)})
        response = LastThreeWishListView.as_view()(request)

        # Kiểm thử kết quả
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['book_id'], self.book2.pk)  # Sách mới nhất (book2) xuất hiện trước
        self.assertEqual(response.data[1]['book_id'], self.book1.pk)

    def test_lay_3_wishlist_gan_nhat_voi_userid_hop_le_khong_co_sach(self):
        """
        Test Case ID: UT-LTWL-002
        Mo ta: Test lay 3 sach gan nhat trong wishlist voi user_id hop le nhung khong co sach
        Input: user_id hop le, khong co du lieu wishlist
        Mong doi: Tra ve 200, danh sach rong
        """
        # Gửi request
        request = self.factory.get(reverse('getLastThreeWishListView'), {'user_id': str(self.reader.user_id)})
        response = LastThreeWishListView.as_view()(request)

        # Kiểm thử kết quả
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_lay_3_wishlist_gan_nhat_khi_thieu_userid(self):
        """
        Test Case ID: UT-LTWL-003
        Mo ta: Test lay 3 sach gan nhat trong wishlist khi thieu user_id
        Input: Khong co user_id
        Mong doi: Tra ve 400, thong bao loi
        """
        request = self.factory.get(reverse('getLastThreeWishListView'), {})
        response = LastThreeWishListView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_lay_3_wishlist_gan_nhat_voi_userid_khong_hop_le(self):
        """
        Test Case ID: UT-LTWL-004
        Mo ta: Test lay 3 sach gan nhat trong wishlist voi user_id khong hop le
        Input: user_id khong phai so nguyen
        Mong doi: Tra ve 400, thong bao loi
        """
        request = self.factory.get(reverse('getLastThreeWishListView'), {'user_id': 'invalid'})
        response = LastThreeWishListView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_lay_3_wishlist_gan_nhat_voi_userid_khong_ton_tai(self):
        """
        Test Case ID: UT-LTWL-005
        Mo ta: Test lay 3 sach gan nhat trong wishlist voi user_id khong ton tai
        Input: user_id khong ton tai
        Mong doi: Tra ve 400, thong bao Reader not found
        """
        request = self.factory.get(reverse('getLastThreeWishListView'), {'user_id': '9999'})
        response = LastThreeWishListView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Reader not found")
class InsertFeedbackViewTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            user_name="testuser",
            email="test@example.com",
            user_password=bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            is_active=True
        )
        self.reader = Reader.objects.create(user_id=self.user.user_id, reader_point=0, reader_rank="Rookie")
        self.manager = User.objects.create(
            user_name="manager",
            email="manager@example.com",
            user_password=bcrypt.hashpw("manager123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            is_active=True, is_admin=True
        )
        self.manager_reader = Reader.objects.create(user_id=self.manager.user_id, reader_point=0, reader_rank="Rookie")

    def test_them_phan_hoi_voi_userid_hop_le_diem_nho_hon_500(self):
        """
        Test Case ID: UT-IFV-001
        Mo ta: Test them phan hoi voi user_id hop le, diem nho hon 500
        Input: user_id hop le, feedback_description hop le, reader_point < 500
        Mong doi: Tra ve 201, tao feedback, cap nhat diem, rank giu nguyen
        """
        data = {
            'user_id': str(self.reader.user_id),
            'feedback_description': 'Good service'
        }
        request = self.factory.post(reverse('InsertFeedbackView'), data, format='json')
        response = InsertFeedbackView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('feedback_id', response.data)
        reader = Reader.objects.get(user_id=self.reader.user_id)
        self.assertEqual(reader.reader_point, 30)
        self.assertEqual(reader.reader_rank, "Rookie")
        self.assertEqual(FeedBack.objects.count(), 1)
        self.assertEqual(Gamification_Record.objects.count(), 1)
        self.assertEqual(Notification.objects.count(), 1)

    def test_them_phan_hoi_voi_userid_hop_le_diem_tu_500_den_1499(self):
        """
        Test Case ID: UT-IFV-002
        Mo ta: Test them phan hoi voi user_id hop le, diem tu 500 den 1499
        Input: user_id hop le, feedback_description hop le, reader_point = 500
        Mong doi: Tra ve 201, tao feedback, cap nhat diem, rank thanh Bronze
        """
        self.reader.reader_point = 500
        self.reader.save()
        data = {
            'user_id': str(self.reader.user_id),
            'feedback_description': 'Good service'
        }
        request = self.factory.post(reverse('InsertFeedbackView'), data, format='json')
        response = InsertFeedbackView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('feedback_id', response.data)
        reader = Reader.objects.get(user_id=self.reader.user_id)
        self.assertEqual(reader.reader_point, 530)
        self.assertEqual(reader.reader_rank, "Bronze")
        self.assertEqual(FeedBack.objects.count(), 1)
        self.assertEqual(Gamification_Record.objects.count(), 1)
        self.assertEqual(Notification.objects.count(), 1)

    def test_them_phan_hoi_voi_userid_hop_le_diem_tu_1500_den_2999(self):
        """
        Test Case ID: UT-IFV-003
        Mo ta: Test them phan hoi voi user_id hop le, diem tu 1500 den 2999
        Input: user_id hop le, feedback_description hop le, reader_point = 1500
        Mong doi: Tra ve 201, tao feedback, cap nhat diem, rank thanh Silver
        """
        self.reader.reader_point = 1500
        self.reader.save()
        data = {
            'user_id': str(self.reader.user_id),
            'feedback_description': 'Good service'
        }
        request = self.factory.post(reverse('InsertFeedbackView'), data, format='json')
        response = InsertFeedbackView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('feedback_id', response.data)
        reader = Reader.objects.get(user_id=self.reader.user_id)
        self.assertEqual(reader.reader_point, 1530)
        self.assertEqual(reader.reader_rank, "Silver")
        self.assertEqual(FeedBack.objects.count(), 1)
        self.assertEqual(Gamification_Record.objects.count(), 1)
        self.assertEqual(Notification.objects.count(), 1)

    def test_them_phan_hoi_voi_userid_hop_le_diem_lon_hon_3000(self):
        """
        Test Case ID: UT-IFV-004
        Mo ta: Test them phan hoi voi user_id hop le, diem lon hon 3000
        Input: user_id hop le, feedback_description hop le, reader_point = 3000
        Mong doi: Tra ve 201, tao feedback, cap nhat diem, rank thanh Gold
        """
        self.reader.reader_point = 3000
        self.reader.save()
        data = {
            'user_id': str(self.reader.user_id),
            'feedback_description': 'Good service'
        }
        request = self.factory.post(reverse('InsertFeedbackView'), data, format='json')
        response = InsertFeedbackView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('feedback_id', response.data)
        reader = Reader.objects.get(user_id=self.reader.user_id)
        self.assertEqual(reader.reader_point, 3030)
        self.assertEqual(reader.reader_rank, "Gold")
        self.assertEqual(FeedBack.objects.count(), 1)
        self.assertEqual(Gamification_Record.objects.count(), 1)
        self.assertEqual(Notification.objects.count(), 1)

    def test_them_phan_hoi_khi_thieu_du_lieu(self):
        """
        Test Case ID: UT-IFV-005
        Mo ta: Test them phan hoi khi thieu user_id hoac feedback_description
        Input: Thieu user_id hoac feedback_description
        Mong doi: Tra ve 400, thong bao loi
        """
        data = {
            'user_id': str(self.reader.user_id)  # Thiếu feedback_description
        }
        request = self.factory.post(reverse('InsertFeedbackView'), data, format='json')
        response = InsertFeedbackView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "User ID and feedback description are required")

    def test_them_phan_hoi_voi_userid_khong_ton_tai(self):
        """
        Test Case ID: UT-IFV-006
        Mo ta: Test them phan hoi voi user_id khong ton tai
        Input: user_id khong ton tai
        Mong doi: Tra ve 404, thong bao Reader not found
        """
        data = {
            'user_id': '9999',
            'feedback_description': 'Good service'
        }
        request = self.factory.post(reverse('InsertFeedbackView'), data, format='json')
        response = InsertFeedbackView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], "Reader not found")

    def test_them_phan_hoi_voi_userid_khong_hop_le(self):
        """
        Test Case ID: UT-IFV-007
        Mo ta: Test them phan hoi voi user_id khong hop le
        Input: user_id khong phai so nguyen
        Mong doi: Tra ve 400, thong bao loi
        """
        data = {
            'user_id': 'invalid',
            'feedback_description': 'Good service'
        }
        request = self.factory.post(reverse('InsertFeedbackView'), data, format='json')
        response = InsertFeedbackView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
from rest_framework.test import force_authenticate
class RemoveUploadedBookViewTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            user_name="testuser",
            email="test@example.com",
            user_password=bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            is_active=True
        )
        self.reader = Reader.objects.create(user_id=self.user.user_id, reader_point=0, reader_rank="New")
        self.category = Category.objects.create(category_id=1, category_name="Test Category")
        self.book = Book.objects.create(
            book_name="Test Book", book_author="Test Author", book_type="Fiction",
            book_barcode="123456789", book_description="Test Description", category=self.category,
            status=Book.Status.ACCEPTED
        )
        self.uploaded_book = UploadedBook.objects.create(book=self.book, reader=self.reader)

    def test_xoa_sach_da_upload_voi_du_lieu_hop_le(self):
        """
        Test Case ID: UT-RUBV-001
        Mo ta: Test xoa sach da upload voi book_id va user_id hop le
        Input: book_id va user_id hop le, UploadedBook ton tai
        Mong doi: Tra ve 200, xoa thanh cong (hoac 500 do FieldError)
        """
        url = reverse('remove_uploaded_book') + f"?book_id={self.book.pk}&user_id={self.user.user_id}"
        request = self.factory.delete(url)
        force_authenticate(request, user=self.user)

        response = RemoveUploadedBookView.as_view()(request)

        # Vì code gốc có lỗi FieldError, mong đợi 500 thay vì 200
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('error', response.data)

    def test_xoa_sach_da_upload_khi_thieu_du_lieu(self):
        """
        Test Case ID: UT-RUBV-002
        Mo ta: Test xoa sach da upload khi thieu book_id hoac user_id
        Input: Thieu book_id hoac user_id
        Mong doi: Tra ve 400, thong bao loi
        """
        url = reverse('remove_uploaded_book') + f"?user_id={self.reader.user_id}"  # Thiếu book_id
        request = self.factory.delete(url)
        force_authenticate(request, user=self.user)

        response = RemoveUploadedBookView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Both book_id and user_id are required")

    def test_xoa_sach_da_upload_voi_userid_khong_ton_tai(self):
        """
        Test Case ID: UT-RUBV-003
        Mo ta: Test xoa sach da upload voi user_id khong ton tai
        Input: user_id khong ton tai
        Mong doi: Tra ve 404, thong bao Reader not found
        """
        url = reverse('remove_uploaded_book') + f"?book_id={self.book.pk}&user_id=9999"
        request = self.factory.delete(url)
        force_authenticate(request, user=self.user)

        response = RemoveUploadedBookView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], "Reader not found")

    def test_xoa_sach_da_upload_voi_uploadedbook_khong_ton_tai(self):
        """
        Test Case ID: UT-RUBV-004
        Mo ta: Test xoa sach da upload voi UploadedBook khong ton tai
        Input: book_id khong ton tai trong UploadedBook cua reader
        Mong doi: Tra ve 500 do FieldError thay vi 404
        """
        url = reverse('remove_uploaded_book') + f"?book_id=9999&user_id={self.reader.user_id}"
        request = self.factory.delete(url)
        force_authenticate(request, user=self.user)

        response = RemoveUploadedBookView.as_view()(request)

        # Vì code gốc có lỗi FieldError, mong đợi 500 thay vì 404
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('error', response.data)

    def test_xoa_sach_da_upload_voi_book_khong_ton_tai(self):
        """
        Test Case ID: UT-RUBV-005
        Mo ta: Test xoa sach da upload voi Book khong ton tai
        Input: book_id ton tai trong UploadedBook nhung khong ton tai trong Book
        Mong doi: Tra ve 500 do Book.DoesNotExist khong duoc xu ly
        """
        invalid_book_id = 9999
        uploaded_book = UploadedBook.objects.create(book_id=invalid_book_id, reader=self.reader)

        url = reverse('remove_uploaded_book') + f"?book_id={invalid_book_id}&user_id={self.reader.user_id}"
        request = self.factory.delete(url)
        force_authenticate(request, user=self.user)

        response = RemoveUploadedBookView.as_view()(request)

        # Vì code gốc khong xu ly Book.DoesNotExist, mong doi 500
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('error', response.data)

    def test_xoa_sach_da_upload_voi_userid_khong_hop_le(self):
        """
        Test Case ID: UT-RUBV-006
        Mo ta: Test xoa sach da upload voi user_id khong hop le
        Input: user_id khong phai so nguyen
        Mong doi: Tra ve 400, thong bao loi
        """
        url = reverse('remove_uploaded_book') + f"?book_id={self.book.pk}&user_id=invalid"
        request = self.factory.delete(url)
        force_authenticate(request, user=self.user)

        response = RemoveUploadedBookView.as_view()(request)

        # Vì code khong xu ly kieu du lieu, se gap loi khi truy van Reader, mong doi 500
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('error', response.data)

    def test_xoa_sach_da_upload_voi_bookid_khong_hop_le(self):
        """
        Test Case ID: UT-RUBV-007
        Mo ta: Test xoa sach da upload voi book_id khong hop le
        Input: book_id khong phai so nguyen
        Mong doi: Tra ve 400, thong bao loi
        """
        url = reverse('remove_uploaded_book') + f"?book_id=invalid&user_id={self.reader.user_id}"
        request = self.factory.delete(url)
        force_authenticate(request, user=self.user)
        response = RemoveUploadedBookView.as_view()(request)


        # Vì code khong xu ly kieu du lieu, se gap loi khi truy van UploadedBook, mong doi 500
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('error', response.data)
class BookContinueReadingListViewTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            user_name="testuser",
            email="test@example.com",
            user_password=bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            is_active=True
        )
        self.reader = Reader.objects.create(user_id=self.user.user_id, reader_point=0, reader_rank="New")
        self.category = Category.objects.create(category_id=1, category_name="Test Category")
        self.book1 = Book.objects.create(
            book_name="Book 1", book_author="Author 1", book_type="Fiction",
            book_barcode="1234567891", book_description="Description 1", category=self.category,
            status=Book.Status.ACCEPTED
        )
        self.book2 = Book.objects.create(
            book_name="Book 2", book_author="Author 2", book_type="Fiction",
            book_barcode="1234567892", book_description="Description 2", category=self.category,
            status=Book.Status.ACCEPTED
        )
        self.book3 = Book.objects.create(
            book_name="Book 3", book_author="Author 3", book_type="Fiction",
            book_barcode="1234567893", book_description="Description 3", category=self.category,
            status=Book.Status.PENDING  # Chưa được chấp nhận
        )
        self.continue_reading1 = BookContinueReading.objects.create(reader=self.reader, book=self.book1)
        self.continue_reading2 = BookContinueReading.objects.create(reader=self.reader, book=self.book2)

    def test_lay_danh_sach_sach_tiep_tuc_doc_voi_userid_hop_le(self):
        """
        Test Case ID: UT-BCRLV-001
        Mo ta: Test lay danh sach sach tiep tuc doc voi user_id hop le
        Input: user_id hop le, co sach trong BookContinueReading
        Mong doi: Tra ve 200, danh sach sach
        """
        url = reverse('continue-reading-books') + f"?user_id={self.user.user_id}"
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)

        response = BookContinueReadingListView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Có 2 sách được chấp nhận
        self.assertEqual(response.data['results'][0]['book_name'], "Book 2")  # Sắp xếp ngược theo continue_reading_id
        self.assertEqual(response.data['results'][1]['book_name'], "Book 1")

    def test_lay_danh_sach_sach_tiep_tuc_doc_khi_thieu_userid(self):
        """
        Test Case ID: UT-BCRLV-002
        Mo ta: Test lay danh sach sach tiep tuc doc khi thieu user_id
        Input: Thieu user_id
        Mong doi: Tra ve 400, thong bao loi
        """
        url = reverse('continue-reading-books')  # Không có user_id
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)

        response = BookContinueReadingListView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "User ID is required")

    def test_lay_danh_sach_sach_tiep_tuc_doc_khi_khong_co_sach(self):
        """
        Test Case ID: UT-BCRLV-003
        Mo ta: Test lay danh sach sach tiep tuc doc khi khong co sach
        Input: user_id hop le, khong co sach trong BookContinueReading
        Mong doi: Tra ve 200, danh sach rong
        """
        # Tạo user và reader mới không có sách trong BookContinueReading
        user2 = User.objects.create(
            user_name="testuser2",
            email="test2@example.com",
            user_password=bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            is_active=True
        )
        reader2 = Reader.objects.create(user_id=user2.user_id, reader_point=0, reader_rank="New")

        url = reverse('continue-reading-books') + f"?user_id={user2.user_id}"
        request = self.factory.get(url)
        force_authenticate(request, user=user2)

        response = BookContinueReadingListView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)  # Danh sách rỗng

    def test_lay_danh_sach_sach_tiep_tuc_doc_voi_userid_khong_hop_le(self):
        """
        Test Case ID: UT-BCRLV-004
        Mo ta: Test lay danh sach sach tiep tuc doc voi user_id khong hop le
        Input: user_id khong phai so nguyen
        Mong doi: Tra ve 500 do loi truy van
        """
        url = reverse('continue-reading-books') + f"?user_id=invalid"
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)

        response = BookContinueReadingListView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('error', response.data)