from django.urls import path
from . import views

urlpatterns = [
    path("jobs/", views.JobListCreate.as_view(), name="job-list"),
    path("jobs/delete/<int:pk>/", views.JobDelete.as_view(), name="delete-job"),
    path("set_webapp_pass",)
]