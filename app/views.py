import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

import requests
from datetime import date

# Create your views here.
login_url = "https://github.com/login/oauth/authorize?client_id=Iv23libtWYyxnUndDKbu&duration=temporary&redirect_uri=https%3A%2F%2Fadventofracket.com%2Fauth&response_type=code&scope=&state=x"

def day_available(day):
    current_date = date.today()
    if current_date.month != 12:
        current_date = date(2025, 12, 1)
    return day <= current_date.day

def index(request):
    if request.method != "GET":
        return JsonResponse({"error": request.method + " not allowed here"}, status=400)
    stars = [{"i": i, "open": day_available(i)} for i in range(1,26)]
    return render(request, "index.jekyll", {
        "stars": stars
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
        "starter_code_part1": starter_code_part1
    })

def submit(request, number):
    pass

@login_required
def settings(request):
    pass

def login_view(request):
    return HttpResponseRedirect(login_url)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def auth(request):
    pass