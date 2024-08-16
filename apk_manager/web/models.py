from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4 as uuid


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


class App(models.Model):
    name = models.CharField(max_length=255, default=uuid().hex)
    version = models.CharField(max_length=50, blank=True, null=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    apk_file = models.FileField(upload_to="apks/")
    first_screen_screenshot = models.ImageField(
        upload_to="screenshots/", blank=True, null=True
    )
    second_screen_screenshot = models.ImageField(
        upload_to="screenshots/", blank=True, null=True
    )
    video_recording = models.FileField(upload_to="recordings/", blank=True, null=True)
    ui_hierarchy = models.FileField(upload_to="ui_hierarchies/", blank=True, null=True)
    screen_changed = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
