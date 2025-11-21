"""
Views for the core app.

This module handles rendering of public-facing pages like landing,
about, and projects pages.
"""

from django.shortcuts import render


def landing_view(request):
    """
    Render the landing page.

    Args:
        request: Django request object

    Returns:
        Rendered landing page template
    """
    return render(request, "core/landing.html")


def about_view(request):
    """
    Render the about page.

    Args:
        request: Django request object

    Returns:
        Rendered about page template
    """
    return render(request, "core/about.html")


def projects_view(request):
    """
    Render the projects page.

    Args:
        request: Django request object

    Returns:
        Rendered projects page template
    """
    return render(request, "core/projects.html")
