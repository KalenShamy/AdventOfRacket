import json
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .models import User, Problem
import requests
from datetime import date
import os
from dotenv import load_dotenv

load_dotenv()

def require_login(request):
    if not request.session.get("user_id"):
        return False, redirect("/login")
    return True, None

def day_available(day):
    current_date = date.today()
    if current_date.month != 12:
        current_date = date(2025, 12, 1)
    return day <= current_date.day

def index(request):
    if request.method != "GET":
        return JsonResponse({"error": request.method + " not allowed here"}, status=400)
    new_user = request.session.get("new_user", False)
    request.session["new_user"] = False
    username = None
    problems = []
    if request.session.get("user_id"):
        username = request.session.get("username")
    stars = [{"i": i, "open": day_available(i)} for i in range(1,26)]
    return render(request, "index.jekyll", {
        "username": username,
        "stars": stars,
        "new_user": new_user
    })

def leaderboard(request, day=None):
    if request.method != "GET":
        return JsonResponse({"error": request.method + " not allowed here"}, status=400)
    
    days = [{"i": i, "open": day_available(i)} for i in range(1,26)]
    
    if day != None and day_available(day):
        leaderboard_two_stars = []  # TODO: Fetch real data
        leaderboard_one_star = []  # TODO: Fetch real data
        return render(request, "leaderboard_specific.jekyll", {
            "days": days, "selected_day": day,
            "leaderboard_two_stars": leaderboard_two_stars,
            "leaderboard_one_star": leaderboard_one_star
        })
    
    if day != None and not day_available(day):
        return HttpResponseRedirect(reverse("leaderboard"))
    
    leaderboard_overall = []  # TODO: Fetch real data
    return render(request, "leaderboard.jekyll", {
        "days": days, "leaderboard_overall": leaderboard_overall
    })

def problem(request, number=None):
    if request.method != "GET":
        return JsonResponse({"error": request.method + " not allowed here"}, status=400)
    
    is_logged_in, redirect_url = require_login(request)
    if not is_logged_in:
        return redirect_url
    
    username = request.session.get("username")

    if number == None:
        current_date = date.today()
        if current_date.month != 12:
            current_date = date(2025, 12, 1)
        number = current_date.day
    
    if not day_available(number):
        return HttpResponseRedirect(reverse("index"))
    
    # Fetch starter code for part 1
    starter_code_part1 = ""
    try:
        response = requests.get(f"http://api.adventofracket.com/starter/{number}/1")
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        starter_code_part1 = response.text
    except requests.exceptions.RequestException as e:
        # Handle connection errors, timeouts, etc.
        print(f"Error fetching starter code: {e}")

    return render(request, "problem.jekyll", {
        "selected_day": number,
        "starter_code_part1": starter_code_part1,
        "username": username
    })

def submit(request, number):
    pass

# GitHub OAuth

def github_login(request):
    github_auth_url = (
        f"https://github.com/login/oauth/authorize?client_id={os.getenv("GITHUB_OAUTH_CLIENT_ID")}&scope=read:user"
    )
    return redirect(github_auth_url)

def github_callback(request):
    code = request.GET.get("code")

    # Exchange code for access token
    token_response = requests.post(
        "https://github.com/login/oauth/access_token",
        data={
            "client_id": os.getenv("GITHUB_OAUTH_CLIENT_ID"),
            "client_secret": os.getenv("GITHUB_OAUTH_CLIENT_SECRET"),
            "code": code,
        },
        headers={"Accept": "application/json"},
    )
    access_token = token_response.json().get("access_token")

    # Fetch user info
    user_response = requests.get(
        "https://api.github.com/user",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    user_data = user_response.json()

    github_id = str(user_data["id"])
    user = User.objects(github_id=github_id).first()

    if not user:
        user = User(github_id=github_id)
        request.session["new_user"] = True

    user.username = user_data["name"] if user_data["name"] else user_data["login"]
    user.url = user_data["html_url"]
    user.avatar_url = user_data["avatar_url"]
    user.access_token = access_token
    user.save()

    # Store login in session
    request.session["user_id"] = str(user.github_id)
    request.session["username"] = user.username
    request.session["user_data"] = user_data

    return redirect("/")  # Redirect to homepage or dashboard

def logout(request):
    request.session.flush()  # Clear all session data
    return redirect("/")  # Redirect to homepage