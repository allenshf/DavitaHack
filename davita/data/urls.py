from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('enter/', views.enter_data, name='enter'),
	path('submit/', views.submit_data, name='submit'),
]