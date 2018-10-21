from . import views
from django.urls import path


app_name = 'bookdb'
urlpatterns = [
	path('home/', views.login_or_register, name='home'),
	path('book/<str:isbn>/', views.book_detail, name='book_detail'),
	path('book/<str:isbn>/rate/', views.rate_book, name='rate_book'),
	path('book/<str:isbn>/comment/', views.comment, name='comment'),
    path('logout/$', views.user_logout, name='logout'),
]
