from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

class UserProfile(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	photo = models.ImageField(upload_to='users')

class Book(models.Model):
	name = models.CharField(max_length=200, null=True, blank=True)
	edition = models.CharField(max_length=50, null=True, blank=True)
	isbn = models.CharField(max_length=20, null=True, blank=True)
	cover = models.ImageField(upload_to='books')

class Comment(models.Model):
	user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	time_of_comment = models.DateTimeField(auto_now_add=True)
	text = models.CharField(max_length=500, null=True, blank=True)

class Rating(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
	rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)], null=True, blank=True)
