from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

class UserProfile(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
	photo = models.ImageField(upload_to='users')

class Book(models.Model):
	name = models.CharField(max_length=200, null=True, blank=True)
	edition = models.CharField(max_length=50, null=True, blank=True)
	isbn = models.CharField(max_length=100, primary_key=True, unique=True)
	cover = models.ImageField(upload_to='books')
	uploader = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='books', null=True, blank=True)

class Comment(models.Model):
	user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_comments')
	book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_comments')
	time_of_comment = models.DateTimeField(auto_now_add=True)
	text = models.CharField(max_length=500, null=True, blank=True)

class Rating(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_ratings')
	user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_ratings')
	rating = models.PositiveIntegerField(validators=[MaxValueValidator(10)], null=True, blank=True)
