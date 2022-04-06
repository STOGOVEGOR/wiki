from django.urls import path

from . import views

urlpatterns = [
#    path("", views.index, name="index"),
    path("wiki", views.index, name="index"),
    path("search", views.search, name="search"),
    path("newentry", views.newentry, name="newentry"),
    path("editentry", views.editentry, name="editentry"),
    path("random_page", views.random_page, name="random_page"),
    path("wiki/<str:title>", views.entry, name="entry")
]
