from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.conf import settings

from .forms import RegisterForm, LoginForm, UpdateUserForm
from .shopee import main as shopee_run
from .tokopedia import main as tokopedia_run
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver

DRIVER_SHOPEE = None
DRIVER_TOKOPEDIA = None
DRIVER_PATH = Service(getattr(settings, "CHROME_DRIVER", None))

options_shopee = Options()
options_shopee.add_argument('--headless')
options_shopee.add_argument('--no-sandbox')
options_shopee.add_argument('--disable-dev-shm-usage')
options_shopee.add_argument('--disable-gpu')
options_shopee.add_argument("window-size=6000,6000")

options_tokopedia = Options()
options_tokopedia.add_argument('--headless')
options_tokopedia.add_argument('--no-sandbox')
options_tokopedia.add_argument('--disable-dev-shm-usage')
options_tokopedia.add_argument('--disable-gpu')
options_tokopedia.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
options_tokopedia.add_argument("window-size=1920,1080")

def handler_404(request, exception):
    return render(request, 'users/404.html')

def home(request):
    return render(request, 'users/home.html')

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)

    return render(request, 'users/profile.html', {'user_form': user_form})

@login_required
def Shopee(request):
    global DRIVER_SHOPEE
    if request.method == 'POST':
        DRIVER_SHOPEE = webdriver.Chrome(service=DRIVER_PATH, chrome_options=options_shopee)
        text = request.POST['product']
        try:
            df = shopee_run(text, DRIVER_SHOPEE)
            return render(request, 'scrape/shopee.html', {'df': df, 'text': text})
        except:
            return HttpResponseBadRequest('Runtime Error')
        finally:
            DRIVER_SHOPEE.close()

    return render(request, 'scrape/shopee.html')

@login_required
def Tokopedia(request):
    global DRIVER_TOKOPEDIA
    if request.method == 'POST':
        DRIVER_TOKOPEDIA = webdriver.Chrome(service=DRIVER_PATH, chrome_options=options_tokopedia)
        text = request.POST['product']
        try:
            df = tokopedia_run(text, DRIVER_TOKOPEDIA)
            return render(request, 'scrape/tokopedia.html', {'df': df, 'text': text})
        except:
            return HttpResponseBadRequest('Runtime Error')
        finally:
            DRIVER_TOKOPEDIA.close()
        
    return render(request, 'scrape/tokopedia.html')

def CancelScrapeShopee(request):
    try:
        time.sleep(5)
        DRIVER_SHOPEE.close()
    except:
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))

def CancelScrapeTokopedia(request):
    try:
        time.sleep(5)
        DRIVER_TOKOPEDIA.close()
    except:
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))