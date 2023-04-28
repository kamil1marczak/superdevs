from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView

from superdevs.starwars.models import Dataset
from superdevs.starwars.services import download_swapi_characters_as_csv, generate_csv_filename, render_dataset

User = get_user_model()


class DatasetListView(ListView):
    template_name = "starwars/datasets_list.html"
    model = Dataset
    context_object_name = "datasets"


dataset_list_view = DatasetListView.as_view()


class DatasetDetailView(LoginRequiredMixin, DetailView):
    model = Dataset
    template_name = "starwars/dataset.html"
    offline = False
    offline_contex = None

    def get_base_kwargs(self):
        self.dataset = self.get_object()
        explore = self.request.GET.get("explore")
        self.explore = explore.split(",") if explore else []
        self.limit = int(self.request.GET.get("limit", default="10"))

    def get_render_dataset(self):
        return render_dataset(dataset_path=self.dataset.path, explore=self.explore, limit=self.limit)

    def get_context_data(self, **kwargs):
        self.get_base_kwargs()
        if not self.offline:
            html, fields, show_load_more = self.get_render_dataset()
        else:
            html, fields, show_load_more = self.offline_contex

        context = {
            "dataset": self.dataset,
            "dataset_html": html,
            "explore": self.explore,
            "fields": fields,
            "limit": self.limit + 10,
            "show_load_more": show_load_more,
        }

        # pprint(context, depth=6)

        context = super().get_context_data(**context)

        return context


dataset_detail_view = DatasetDetailView.as_view()


class DatasetDownloadRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False
    http_method_names = [
        "get",
    ]
    mock_swapi = False
    people_data = None
    planet_data = None
    file_path = None
    dataset = None

    def download_swapi_to_csv(self):
        if not self.file_path:
            self.file_path = generate_csv_filename()
        if not self.mock_swapi:
            assert (
                download_swapi_characters_as_csv(
                    path=self.file_path, people_data=self.people_data, planet_data=self.planet_data
                )
                == self.file_path
            )
        self.dataset, self.created = Dataset.objects.get_or_create(path=self.file_path, is_deleted=False)
        return self.dataset

    def get_redirect_url(self, *args, **kwargs):
        return reverse("starwars:dataset_list")

    def get(self, request, *args, **kwargs):
        self.download_swapi_to_csv()
        if self.created:
            messages.success(request, f"Added new dataset fetched on {self.dataset.created_at:%c}.")
        else:
            messages.error(request, f"Dataset at: {self.dataset.path} already exists.")
        return super().get(request, *args, **kwargs)


dataset_download_redirect_view = DatasetDownloadRedirectView.as_view()
