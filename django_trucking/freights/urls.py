from django.urls import path

from . import views


urlpatterns = [
path("", views.FreightsView.as_view()),
path("filter/", views.FilterFreightsView.as_view(), name='filter'),
path("<slug:slug>/", views.FreightDetailView.as_view(), name="freight_detail"),
path("review/<int:pk>/", views.AddReview.as_view(), name="add_review"),
path("worker/<str:slug>/", views.WorkerView.as_view(), name="worker_detail"),

]