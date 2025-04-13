#-- add rating and review
from django.shortcuts import redirect, render

# pip install djangorestframework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from .models import *
from .serializers import *

# pip install djangorestframework-jwt
import jwt
import datetime

# pip install django-bcrypt
import bcrypt

#--------
# pip install urlsafe-base64-py
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
#---------
from .pagination import *
from django.http import JsonResponse
from django.db.models import Q
from django.db.models import Avg
from django.db.models import Count
from django.db.models import Case, When, Value
from django.db.utils import IntegrityError

#----------
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import timezone
from django.contrib import messages
class AddRatingAndReviewView(APIView):
    def post(self, request):
        # Extract data from request
        book_id = request.data.get("book_id")
        user_id = request.data.get("user_id")
        rating = request.data.get("rating")
        review = request.data.get("review")

        # Validate that required fields are present
        if not (book_id and user_id and rating is not None and review):
            return Response({"error": "All fields (book_id, user_id, rating, review) are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Validate rating range
        if not (1 <= rating <= 5):
            return Response({"error": "Rating must be between 1 and 5."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Fetch the book and reader objects
        try:
            book = Book.objects.get(pk=book_id)
            reader = Reader.objects.get(user_id=user_id)
        except Book.DoesNotExist:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)
        except Reader.DoesNotExist:
            return Response({"error": "Reader not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if book is accepted
        if book.status != Book.Status.ACCEPTED:
            return Response({"error": "Cannot review a book that is not accepted."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Check for duplicate review
        if Rating_And_Review.objects.filter(book=book, reader=reader).exists():
            return Response({"error": "You have already reviewed this book."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Create the Rating_And_Review entry
        Rating_And_Review.objects.create(
            book=book,
            reader=reader,
            rating=rating,
            review=review
        )

        # Recalculate the average rating for the book
        ratings = Rating_And_Review.objects.filter(book=book).values_list('rating', flat=True)
        total_ratings = sum(ratings)
        rating_count = len(ratings)
        average_rating = round(total_ratings / rating_count) if rating_count > 0 else 0

        # Update the book's average rating
        book.book_rating_avg = average_rating
        book.save()

        # Update reader points
        reader.reader_point += 20
        if(reader.reader_point>=500 and reader.reader_point<1500):
            reader.reader_rank="Bronze"
        elif(reader.reader_point>=1500 and reader.reader_point<3000):
            reader.reader_rank="Silver"
        elif(reader.reader_point>=3000):
            reader.reader_rank="Gold"

        reader.save()

        # Insert new gamification record
        Gamification_Record.objects.create(
            reader_id=reader.reader_id,
            gamification_description="Rating And Review Book Achievement",
            achieved_point=20
        )

        Notification.objects.create(
            reader_id=reader.reader_id,
            manager_id=2,
            notification_record="+20 Point for Rating And Review Book",
            notification_title="New Point Achievement"
        )

        return Response({"message": "Rating and review added successfully."}, status=status.HTTP_201_CREATED)