# Generated by Django 4.2.15 on 2024-08-16 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0002_app"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="app",
            name="uploaded_at",
        ),
        migrations.AddField(
            model_name="app",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="app",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
