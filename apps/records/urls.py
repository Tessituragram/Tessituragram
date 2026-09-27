from django.urls import path
from . import views
from .export import export_database
 
app_name = "records"
 
urlpatterns = [
    path("soloistic_search/", views.soloistic_search, name="soloistic_search"),
    path("record/<uuid:group_id>/", views.record_detail, name="record_detail"),
    path("<int:pk>/midi/", views.midi_download, name="midi_download"),
    path("<int:pk>/delete/", views.delete_record, name="delete_record"),
    path("deleted/", views.deleted_list, name="deleted_list"),
    path("reinstate/<uuid:submission_group>/", views.reinstate_record, name="reinstate_record"),
    path("export/", export_database, name="export_database"),
    path(
        "graphic/<uuid:submission_group>/<str:clef>/<str:graphic_type>/",
        views.record_graphic,
        name="record_graphic",
    ),
]