from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.conf import settings
from django.core.cache import cache

from .forms import RegisterForm, LoginForm, UpdateUserForm
from .shopee import main as shopee_run
from .tokopedia import main as tokopedia_run
import time
import random
import string
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver

DRIVER_PATH = Service(getattr(settings, "CHROME_DRIVER", None))

# Setup Chrome options for both Shopee and Tokopedia
def get_chrome_options(platform):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument("window-size=6000,6000" if platform == 'shopee' else "window-size=1920,1080")
    
    if platform == 'tokopedia':
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
    
    return options

def generate_random_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

def handler_404(request, exception):
    return render(request, 'users/404.html')

def home(request):
    return render(request, 'users/home.html')

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='/')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account created for {form.cleaned_data.get("username")}')
            return redirect(to='login')
        return render(request, self.template_name, {'form': form})

class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super().form_valid(form)

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
def scrape_platform(request, platform, random_id=None):
    if platform not in ['shopee', 'tokopedia']:
        return HttpResponseBadRequest('Invalid platform specified.')

    driver = None
    global DRIVER_SHOPEE, DRIVER_TOKOPEDIA

    cache_key = f'scrape_{platform}_{random_id}' if random_id else f'scrape_{platform}_{generate_random_id()}'
    
    if random_id:
        scrape_data = cache.get(cache_key)
        if not scrape_data:
            return redirect(platform)
    else:
        random_id = generate_random_id()

    if request.method == 'POST':
        driver = webdriver.Chrome(service=DRIVER_PATH, options=get_chrome_options(platform))
        text = request.POST['product']
        try:
            if platform == 'shopee':
                df = shopee_run(text, driver)
            else:
                df = tokopedia_run(text, driver)
            cache.set(cache_key, df, timeout=600)
            return redirect(reverse(platform, kwargs={'random_id': random_id}))
        except Exception as e:
            return HttpResponseBadRequest(f'Runtime Error: {e}')
        finally:
            if driver:
                driver.close()

    scrape_data = cache.get(cache_key, None)
    return render(request, f'scrape/{platform}.html', {'df': scrape_data})

@login_required
def Shopee(request, random_id=None):
    return scrape_platform(request, 'shopee', random_id)

@login_required
def Tokopedia(request, random_id=None):
    return scrape_platform(request, 'tokopedia', random_id)

def cancel_scrape(request, platform):
    driver = DRIVER_SHOPEE if platform == 'shopee' else DRIVER_TOKOPEDIA
    try:
        time.sleep(5)
        driver.close()
    except:
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))

def CancelScrapeShopee(request):
    return cancel_scrape(request, 'shopee')

def CancelScrapeTokopedia(request):
    return cancel_scrape(request, 'tokopedia')