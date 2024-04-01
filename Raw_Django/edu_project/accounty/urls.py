from django.urls import path

from . views import (
    registration_view,
    logout_view,
    login_view,
    home,
    profile_view,
	
)

urlpatterns = [
    path('home/', home, name='home'),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('register/', registration_view, name="register"),
    path('profile', profile_view, name='profile'),
    
    
]
