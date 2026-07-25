from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("contact/", views.contact, name="contact"),
    path("contact/success/", views.contact_success, name="contact_success"),
    path("instructions/", views.InstructionsView.as_view(), name="instructions"),
    path("methodology/", views.MethodologyView.as_view(), name="methodology"),
    
]