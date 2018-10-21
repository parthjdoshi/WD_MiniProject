from django.shortcuts import render
from .models import *
from django.db.models import Max, Avg
from django.contrib.auth import login, authenticate

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
				return render(request, 'bookdb/index.html', {'error': 'Incorrect username or password'})
	else:
		user = request.user
		if not user.is_authenticated:
			# TODOO: return some random isbn numbers here
			return render(request, 'bookdb/index.html', {})
		else:
			# TODOO: return some specific recommendations here
			return render(request, 'bookdb/index.html', {})

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
