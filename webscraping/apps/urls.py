from django.urls import path
from .views import home, profile, RegisterView, shopee_scrape, tokopedia_scrape

urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('shopee/', shopee_scrape, name='shopee-scrape'),
    path('tokopedia/', tokopedia_scrape, name='tokopedia-scrape')
]
