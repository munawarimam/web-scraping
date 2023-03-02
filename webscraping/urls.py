from django.contrib import admin

from django.urls import path, include, re_path

from django.conf import settings
from django.conf.urls import handler404
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from apps.views import CustomLoginView, ChangePasswordView

from apps.forms import LoginForm

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('apps.urls')),

    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='users/login.html',
                                           authentication_form=LoginForm), name='login'),

    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    path('password-change/', ChangePasswordView.as_view(), name='password_change'),

    re_path(r'^oauth/', include('social_django.urls', namespace='social')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'apps.views.handler_404'