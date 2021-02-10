from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('enter/', views.enter_data, name='enter'),
	path('submit/', views.submit_data, name='submit'),
	path('submit/<int:id>/', views.submit_data, name='submit'),
	path('upload/', views.upload_image, name='upload'),
	path('confirm/<int:id>/', views.confirm, name='confirm'),
	path('data/', views.data, name='data'),
]