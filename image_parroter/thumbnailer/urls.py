# thumbnailer/urls.py

from django.urls import path

from . import views

urlpatterns = [
  path('', views.HomeView.as_view(), name='home'),
  path('task/<str:task_id>/', views.TaskView.as_view(), name='task'),
]
