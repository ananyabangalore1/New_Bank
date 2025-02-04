from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    path('login/',LoginView.as_view(template_name='user_profile/login.html'), name='login'),
    path('login_success/',views.login_success, name='login_success'),  # Login success redirects to profile
    path('profile/<str:username>/', views.profile, name='user_profile'),
    path('profile/update/',views.generate_ui, name='update_ui'),  # Update UI via SnapSynth
]

