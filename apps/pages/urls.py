from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("people/", views.PeopleView.as_view(), name="people"),
    path("mission/", views.MissionView.as_view(), name="mission"),
    path("background/", views.BackgroundView.as_view(), name="background"),
    path("bibliography/", views.BibliographyView.as_view(), name="bibliography"),
    path("methodology/", views.MethodologyView.as_view(), name="methodology"),
    path("instructions", views.InstructionsView.as_view(), name="instructions"),
    path("future/", views.ProjectsView.as_view(), name="future"),
    path("contact/", views.contact, name="contact"),
    path("contact/success/", views.contact_success, name="contact_success"),
]