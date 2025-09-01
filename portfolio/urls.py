from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    ProjectListView, ProjectDetailView,
    ProjectCreateView, ProjectUpdateView, ProjectDeleteView,
    contact_view
)

urlpatterns = [
    path("", ProjectListView.as_view(), name="project_list"),
    path("projects/<int:pk>/", ProjectDetailView.as_view(), name="project_detail"),

    # Admin/staff CRUD
    path("projects/create/", ProjectCreateView.as_view(), name="project_create"),
    path("projects/<int:pk>/edit/", ProjectUpdateView.as_view(), name="project_update"),
    path("projects/<int:pk>/delete/", ProjectDeleteView.as_view(), name="project_delete"),

    # Contact
    path("contact/", contact_view, name="contact"),
     path("logout/", LogoutView.as_view(next_page="project_list"), name="logout"),
]
