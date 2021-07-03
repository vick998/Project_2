from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listentry", views.listentry, name="listentry"),
    path("<int:listing_id>", views.listingpage, name="listingpage"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("category", views.category, name="category")
]
