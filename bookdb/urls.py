from . import views
from django.urls import path


app_name = 'bookdb'
urlpatterns = [
	path('home/', views.login_or_register, name='home'),
]
