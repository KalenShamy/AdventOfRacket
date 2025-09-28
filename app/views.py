import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from datetime import date

# Create your views here.
login_url = "https://github.com/login/oauth/authorize?client_id=Iv23libtWYyxnUndDKbu&duration=temporary&redirect_uri=https%3A%2F%2Fadventofracket.com%2Fauth&response_type=code&scope=&state=x"

def day_available(day):
    current_date = date.today()
    if current_date.month != 12:
        current_date = date(2025, 12, 1)
    return day <= current_date.day

def index(request):
    stars = [{"i": i, "open": day_available(i)} for i in range(1,26)]
    return render(request, "index.html", {
        "stars": stars
    })

def problem(request, number=None):
    pass

def submit(request, number):
    pass

def leaderboard(request):
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