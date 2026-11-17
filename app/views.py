from django.shortcuts import get_object_or_404, render

from .middleware import HealthMiddleware
from .models import Project, Technology

# /health is answered by HealthMiddleware; this is only for the URL name.
health = HealthMiddleware(lambda request: None)


def home(request):
    projects = Project.objects.filter(published=True).prefetch_related("technologies")
    active = None
    slug = request.GET.get("tech", "")
    if slug:
        active = Technology.objects.filter(slug=slug).first()
        if active:
            projects = projects.filter(technologies=active)
    techs = Technology.objects.filter(projects__published=True).distinct()
    return render(request, "app/home.html", {"projects": projects, "techs": techs, "active": active})


def detail(request, slug):
    project = get_object_or_404(Project.objects.prefetch_related("technologies"), slug=slug, published=True)
    return render(request, "app/detail.html", {"project": project})
