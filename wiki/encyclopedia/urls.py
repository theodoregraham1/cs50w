from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("add/", views.add, name="add"),
    path("search/", views.search, name="search"),
    path("wiki/<str:title>/", views.wiki, name="wiki"),
]
