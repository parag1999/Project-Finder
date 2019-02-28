from django.urls import path
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from project_finder_web_app import views

urlpatterns = [
    path('login/', views.UserLoginAPIView.as_view(), name='login'),
    path('register/', csrf_exempt(views.UserCreateAPIView.as_view()), name='register'),
    path('detail/', views.UserDetailViewSet.as_view({'get': 'list'}), name='detail'),
]
