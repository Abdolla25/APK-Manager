import os
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, ProfileForm, AppForm
from .models import Profile, App
from .utils import extract_apk_metadata


def index_view(request):
    return render(request, "web/index.html")


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "You have been signed up.")
            return redirect("profile")
    else:
        form = SignUpForm()
    return render(request, "web/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "You have been logged in.")
            return redirect("profile")
    else:
        form = AuthenticationForm()
    return render(request, "web/login.html", {"form": form})


@login_required(login_url="login")
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, "web/profile.html", {"profile": profile})


@login_required(login_url="login")
def profile_edit_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been updated.")
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "web/profile_edit.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("index")


@login_required(login_url="login")
def app_list_view(request):
    apps = App.objects.filter(uploaded_by=request.user)
    return render(request, "web/app_list.html", {"apps": apps})


@login_required(login_url="login")
def app_upload_view(request):
    if request.method == "POST":
        form = AppForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.uploaded_by = request.user
            app.save()

            apk_path = os.path.join(settings.MEDIA_ROOT, app.apk_file.name)
            metadata = extract_apk_metadata(apk_path)
            app.name = f"{metadata['name']} - {metadata['package_name']}"
            app.version = metadata["version"]
            app.save()
            messages.success(request, "App has been uploaded.")
            return redirect("app_list")
    else:
        form = AppForm()
    return render(request, "web/app_upload.html", {"form": form})


@login_required(login_url="login")
def app_detail_view(request, pk):
    app = get_object_or_404(App, pk=pk, uploaded_by=request.user)
    return render(request, "web/app_detail.html", {"app": app})


@login_required(login_url="login")
def app_delete_view(request, pk):
    app = get_object_or_404(App, pk=pk, uploaded_by=request.user)
    if request.method == "POST":
        app.delete()
        messages.success(request, "App has been deleted.")
        return redirect("app_list")
    return render(request, "web/app_confirm_delete.html", {"app": app})


def app_run_view(request, pk):
    from .appium_utils import test_android_run
    import threading

    app = get_object_or_404(App, pk=pk)
    threading.Thread(
        target=test_android_run,
        kwargs={
            "apk_path": os.path.join(settings.MEDIA_ROOT, app.apk_file.name),
            "device_id": os.environ.get("ANDROID_DEVICE_ID"),
            "app_package": app.name.split(" - ")[1],
            "app": app,
            "screenshot_path": os.path.join(settings.MEDIA_ROOT, "screenshots"),
            "recording_path": os.path.join(settings.MEDIA_ROOT, "recordings"),
        },
    ).start()
    messages.success(
        request,
        "App has been started on the device. Check the app page for updates within 5 minutes.",
    )
    return redirect("app_detail", pk=pk)
