from django.urls import path, re_path
from .views import home, profile, RegisterView, shopee, tokopedia

urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('shopee/', shopee, name='shopee'),
    path('tokopedia/', tokopedia, name='tokopedia')
]
