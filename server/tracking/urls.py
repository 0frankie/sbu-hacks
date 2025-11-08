from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("track", views.track),
    path("all", views.all),
    path("get/<int:id>", views.get),
    path("delete/<int:id>", views.delete),
    path("thumbnail/<int:id>", views.thumbnail),
]
