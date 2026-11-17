from django.conf import settings
from django.db import models


class Profile(models.Model):
    """Links a Django user to the login service's user (the OIDC `sub`)."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    oidc_sub = models.CharField(max_length=255, unique=True)


class Heartbeat(models.Model):
    """Written by the example job (platform.yaml `jobs.heartbeat`)."""
    at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-at"]


class Technology(models.Model):
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=70, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "technologies"

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=110, unique=True)
    summary = models.CharField(max_length=300, help_text="Short description shown on the card.")
    description = models.TextField(blank=True, help_text="Longer text for the detail page (plain text).")
    url = models.URLField(blank=True, help_text="Live site.")
    repo_url = models.URLField(blank=True)
    screenshot_url = models.URLField(blank=True, help_text="Link to an image.")
    technologies = models.ManyToManyField(Technology, blank=True, related_name="projects")
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers first.")
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name
