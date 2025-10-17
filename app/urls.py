from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("problem/<int:day>/<int:part>", views.problem, name="problem"),
    path("problem/<int:day>/<int:part>/submit", views.submit, name="submit"),
    path("leaderboard", views.leaderboard, name="leaderboard"),
    path("leaderboard/<int:day>", views.leaderboard, name="leaderboard"),

    path("login", views.github_login, name="github_login"),
    path("callback", views.github_callback, name="github_callback"),
    path("logout", views.logout, name="logout"),
]