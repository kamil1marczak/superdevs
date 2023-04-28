from django.urls import path

from superdevs.starwars.views import dataset_detail_view  # dataset,; download,; dataset_list,
from superdevs.starwars.views import dataset_download_redirect_view, dataset_list_view

app_name = "starwars"

urlpatterns = [
    # path("", dataset_list, name="dataset_list"),
    path("", dataset_list_view, name="dataset_list"),
    # path("dataset/<uuid:pk>/", dataset, name="dataset"),
    path("dataset/<uuid:pk>/", dataset_detail_view, name="dataset"),
    # path("download/", download, name="download"),
    path("download/", dataset_download_redirect_view, name="download"),
]
