from django.urls import path

from . import views


urlpatterns = [
path("", views.FreightsView.as_view()),
path("<slug:slug>/", views.FreightDetailView.as_view(), name="freight_detail"),
path("review/<int:pk>/", views.AddReview.as_view(), name="add_review"),

]