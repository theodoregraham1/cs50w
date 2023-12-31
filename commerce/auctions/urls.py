from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add", views.add, name="add"),
    path("listing/<id>", views.listing_view, name="listing"),
    path("bid", views.add_bid, name="add_bid"),
    path("watchlist/<id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("close/<id>", views.close, name="close"),
    path("comment", views.comment, name="comment"),
    path("categories", views.categories, name="categories"),
    path("category/<name>", views.category, name="category"),
]
