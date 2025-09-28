from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("problem/<int:number>", views.problem, name="problem"),
    path("problem/", views.problem, name="problem"),
    path("problem/<int:day>/submit", views.submit, name="submit"),
    path("leaderboard", views.leaderboard, name="leaderboard"),
    path("leaderboard/<int:day>", views.leaderboard, name="leaderboard"),
    #path("search", views.search, name="search"),
    #path("profile", views.profile, name="profile"),
    #path("profile/edit", views.edit_profile, name="edit_profile"),
    #path("profile/<str:username>", views.profile, name="profile"),

    path("auth", views.auth, name="auth"),
    path("settings", views.settings, name="settings"),

    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
]