from django.shortcuts import render
from .models import Project


def home(request):
    """Home page view."""
    return render(request, "home.html")


def projects(request):
    """
    Single projects page.
    Shows all projects with full details inline.
    """
    projects = Project.objects.all()
    return render(request, "pages/list.html", {
        "projects": projects
    })
