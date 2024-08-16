from django.urls import path
from .views import (
    index_view,
    signup_view,
    login_view,
    logout_view,
    profile_view,
    profile_edit_view,
    app_list_view,
    app_upload_view,
    app_detail_view,
    app_delete_view,
)

urlpatterns = [
    path("", index_view, name="index"),
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),
    path("profile/edit/", profile_edit_view, name="profile_edit"),
    path("apps/", app_list_view, name="app_list"),
    path("apps/upload/", app_upload_view, name="app_upload"),
    path("apps/<int:pk>/", app_detail_view, name="app_detail"),
    path("apps/<int:pk>/delete/", app_delete_view, name="app_delete"),
]
