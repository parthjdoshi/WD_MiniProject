from django.shortcuts import render
from .models import *
from django.db.models import Max, Avg
from django.contrib.auth import login, authenticate
import random
from recombee_api_client.api_client import RecombeeClient
from recombee_api_client.exceptions import APIException
from recombee_api_client.api_requests import *

client = RecombeeClient('wd-project', 'DDf4VljyLxNsbdLtWT1jueFbVsanOWCwbEW59cTpp1W3LB3JlpeT3jqZQ1k7S7sN')

def home(request):
	return render(request, 'index.html', {})

def login_or_register(request):
	if request.method == 'POST':
		data = request.POST
		if data.get('flag', '') == 'register':
			uid = User.objects.aggregate(Max('id'))['id__max'] + 1
			username = data.get('username', '')
			# [TODO] show an appropriate error message in case of same username
			if username == '' or User.objects.filter(usnername=username).count() > 0:
				return render(request, 'index.html', {'error': 'Repeated username'})
			user = User(id=uid)
			user.username = username
			user.set_password(data.get('password', ''))
			user.first_name = data.get('first_name', '')
			user.last_name = data.get('last_name', '')
			user.save()
			profile = UserProfile(user=user)
			profile.photo = request.FILES.get('photo', '')
			profile.save()
			login(request, user)
			return redirect('bookdb:home')
		elif data.get('flag', '') == 'login':
			username = data.get('username', '')
			password = data.get('password', '')
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('bookdb:home')
			else:
				return render(request, 'index.html', {'error': 'Incorrect username or password'})
	else:
		user = request.user
		list_of_isbns = []
		if not user.is_authenticated():
			# TODO: return some random isbn numbers here
			list_of_books = Book.objects.all().order_by("?")[:10]
			
			for book in list_of_books:
				list_of_isbns.append(book.isbn)
			return render(request, 'index.html', {'list_of_isbns': list_of_isbns})
		else:
			# TODO: return some specific recommendations here
			recommended = client.send(RecommendItemsToUser(user.id, 10))
			for r in recommended['recomms']:
				list_of_isbns.append(r.get('id',''))
			return render(request, 'index.html', {'recommended': list_of_isbns})

def book_detail(request, isbn):
	if not request.user.is_authenticated:
		return redirect('bookdb:home')
	try:
		book = Book.objects.get(isbn=isbn)
		comments = Comment.objects.filter(book=book).order_by('-time_of_comment')
		avg_rating = Rating.objects.filter(book=book).aggregate(Avg('rating'))['rating__avg']
		return render(request, 'book_detail.html', {'isbn': isbn, 'comments': comments, 'avg_rating': avg_rating})
	except Exception as e:
		print(e)
	return redirect('bookdb:home')
