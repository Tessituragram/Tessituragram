from django.urls import path
from . import views

app_name = "submissions"

urlpatterns = [
    path("", views.submit_form, name="submit_form"),
    path("success/", views.submission_success, name="submission_success"),
    path("review/", views.review_list, name="review_list"),
    path("review/<int:pk>/", views.review_detail, name="review_detail"),
    path("<int:pk>/edit/", views.edit_resubmit, name="edit_resubmit"),
]
