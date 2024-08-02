from django.urls import path
from .views import home, profile, RegisterView, Shopee, Tokopedia, CancelScrapeShopee, CancelScrapeTokopedia

urlpatterns = [
    path('', home, name='users-home'),
    # path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('shopee/', Shopee, name='shopee'),
    path('tokopedia/', Tokopedia, name='tokopedia'),
    path('cancel-scrape-shopee', CancelScrapeShopee, name='cancel-scrape-shopee'),
    path('cancel-scrape-tokopedia', CancelScrapeTokopedia, name='cancel-scrape-tokopedia'),
]