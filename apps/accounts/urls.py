from django.urls import path, include
from . import views

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("signup/", views.signup, name="signup"),
    path("verify/<uuid:token>/", views.verify_email, name="verify_email"),
    path("profile/", views.profile, name="profile"),
    path(
        "verify-email-change/<uuid:token>/",
        views.verify_email_change,
        name="verify_email_change",
    ),
]
