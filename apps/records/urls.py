from django.urls import path
from . import views
from .export import export_database

app_name = "records"

urlpatterns = [
    path("", views.database, name="database"),
    path("<int:pk>/", views.record_detail, name="record_detail"),
    path("<int:pk>/midi/", views.midi_download, name="midi_download"),
    path("<int:pk>/delete/", views.delete_record, name="delete_record"),
    path("deleted/", views.deleted_list, name="deleted_list"),
    path("<int:pk>/reinstate/", views.reinstate_record, name="reinstate_record"),
    path("export/", export_database, name="export_database"),
]