from django.urls import path
from .views import (
    index_view,
    signup_view,
    login_view,
    logout_view,
    profile_view,
    profile_edit_view,
)

urlpatterns = [
    path("", index_view, name="index"),
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),
    path("profile_edit/", profile_edit_view, name="profile_edit"),
]
