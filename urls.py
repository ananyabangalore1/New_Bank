from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

# Redirect root URL to the login page
def home(request):
    return redirect('login')  # Redirect to the login page

urlpatterns = [
    path('', home, name='home'),  # Root path redirects to login page
    path('admin/', admin.site.urls),  # Admin page URL
    path('login/', include('django.contrib.auth.urls')),  # Built-in login view
    path('user/', include('user_profile.urls')),  # Include user profile URLs (if any)
]

