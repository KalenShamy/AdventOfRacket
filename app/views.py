import json
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .models import User, Problem
from .validate import validate_code
import requests
from datetime import date, datetime
import os
from dotenv import load_dotenv

load_dotenv()

TIME_TO_READ = 31 # seconds

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
    user = None
    stars = [{"i": i, "open": day_available(i), "completion": 1} for i in range(1,26)]
    if request.session.get("user_id"):
        user = User.objects(github_id=request.session.get("user_id")).first()
        # 1 if part1 next, 2 if part2 next, 3 if both done
        for i in range(len(user.problems)):
            stars[i]["completion"] = 1+sum([problem.correct for problem in user.problems[i]])
    if request.session.get("user_id"):
        username = request.session.get("username")
    return render(request, "index.jekyll", {
        "username": username,
        "stars": stars,
        "new_user": new_user,
    })

def leaderboard(request, day=None):
    if request.method != "GET":
        return JsonResponse({"error": request.method + " not allowed here"}, status=400)
    
    days = [{"i": i, "open": day_available(i)} for i in range(1,26)]
    
    if day != None and day_available(day):
        leaderboard_two_stars = Problem.objects(day=day, part=2, correct=True).order_by("total_time")
        leaderboard_one_star = Problem.objects(day=day, part=1, correct=True).order_by("time_taken")
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

def problem(request, day, part=1):
    if request.method != "GET":
        return JsonResponse({"error": request.method + " not allowed here"}, status=400)
    
    is_logged_in, redirect_url = require_login(request)
    if not is_logged_in:
        return redirect_url
    
    username = request.session.get("username")
    
    if not day_available(day):
        return HttpResponseRedirect(reverse("index"))
    
    # check if completed
    started_problem = Problem.objects(player=username, day=day, part=part).first()
    
    # fetch test cases
    test_cases = ""
    try:
        response = requests.get(f"https://api.adventofracket.com/tests/{day}/{part}",
                                headers={"X-Authorization": f"Bearer {os.getenv('AOR_MANAGER_ACCESS_TOKEN')}"})
        response.raise_for_status()
        test_cases = json.loads(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching test cases: {e}")
        return HttpResponse("Fetch Error 1", status=500)

    # fetch starter code
    starter_code = ""
    try:
        response = requests.get(f"https://api.adventofracket.com/starter/{day}/{part}")
        response.raise_for_status()
        starter_code = response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching starter code: {e}")
        return HttpResponse("Fetch Error 2", status=500)

    if started_problem and started_problem.code:
        starter_code = started_problem.code
    elif not started_problem:
        # create a new problem entry if not started
        new_problem = Problem(player=username, day=day, part=part)
        new_problem.save()
        user = User.objects(github_id=request.session.get("user_id")).first()
        if len(user.problems) < day:
            user.problems.append([new_problem])
        else:
            user.problems[day-1].append(new_problem)
        user.save()
        started_problem = new_problem
    if part != 1:
        previous_problem = Problem.objects(player=username, day=day, part=1, correct=True).first()
        if not previous_problem:
            # redirect to part 1 if not completed
            return HttpResponseRedirect(reverse("problem", args=[day, 1]))
        starter_code = starter_code + "\n\n" + previous_problem.code


    for i in range(len(test_cases["public"])):
        test = test_cases["public"][i]
        if started_problem and started_problem.tests and i < len(started_problem.tests):
            test_cases["public"][i] = {"input": test[0], "expected": test[1], "output": started_problem.tests[i]}
        else:
            test_cases["public"][i] = {"input": test[0], "expected": test[1]}

    is_completed = started_problem.correct if started_problem else False

    return render(request, "problem.jekyll", {
        "selected_day": day,
        "selected_part": part,
        "starter_code": starter_code,
        "username": username,
        "is_completed": is_completed,
        "time_taken": started_problem.time_taken if is_completed else False,
        "time_started": started_problem.time_started.timestamp() + TIME_TO_READ,

        "tests": render(request, "tests.jekyll", {
            "test_cases": test_cases["public"],
            "tests_message": started_problem.tests_message if started_problem and started_problem.tests_message and len(started_problem.tests_message) > 0 else None,
        }).content.decode('utf-8'),
    })

def submit(request, day, part=1):
    if request.method != "POST":
        return JsonResponse({"error": request.method + " not allowed here"}, status=400)
    
    is_logged_in, redirect_url = require_login(request)
    if not is_logged_in:
        return redirect_url
    user = User.objects(github_id=request.session.get("user_id")).first()
    problem = Problem.objects(player=user.username, day=day, part=part).first()
    if not problem:
        return JsonResponse({"error": "Problem not started yet"}, status=400)
    if problem.correct:
        return JsonResponse({"error": "Problem already completed"}, status=400)

    code = json.loads(request.body).get("code", "")
    
    # fetch test cases
    test_cases = {"public": [], "private": []}
    try:
        response = requests.get(f"https://api.adventofracket.com/tests/{day}/{part}",
                                headers={"X-Authorization": f"Bearer {os.getenv('AOR_MANAGER_ACCESS_TOKEN')}"})
        response.raise_for_status()
        test_cases = json.loads(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching test cases: {e}")
        return HttpResponse("Fetch Error 3", status=500)
    
    passed, tests_status = validate_code(code, test_cases)
    problem.code = code
    problem.tests = tests_status.get("results", [])
    problem.tests_message = tests_status.get("message", "Unknown error")

    for i in range(len(test_cases["public"])):
        test = test_cases["public"][i]
        if problem and problem.tests and i <= len(problem.tests):
            test_cases["public"][i] = {"input": test[0], "expected": test[1], "output": problem.tests[i]}
        else:
            test_cases["public"][i] = {"input": test[0], "expected": test[1]}

    tests_html = render(request, "tests.jekyll", {
        "test_cases": test_cases["public"],
        "tests_message": problem.tests_message if problem and problem.tests_message and len(problem.tests_message) > 0 else None,
    }).content.decode('utf-8')

    if passed:
        problem.correct = True
        problem.time_taken = -TIME_TO_READ + int(datetime.now().timestamp() - problem.time_started.timestamp())
        if problem.time_taken < 0:
            return JsonResponse({"error": "Please read the problem"}, status=400)
        if part == 2:
            part1_problem = Problem.objects(player=user.username, day=day, part=1).first()
            problem.total_time = problem.time_taken + part1_problem.time_taken
    problem.save()
    return JsonResponse({"success": passed, "tests_html": tests_html}, status=200)
    

# GitHub OAuth

def github_login(request):
    github_auth_url = (
        f"https://github.com/login/oauth/authorize?client_id={os.getenv('GITHUB_OAUTH_CLIENT_ID')}&scope=read:user"
    )
    return redirect(github_auth_url)

def github_callback(request):
    code = request.GET.get("code")

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

    # store login in session
    request.session["user_id"] = str(user.github_id)
    request.session["username"] = user.username
    request.session["user_data"] = user_data

    return redirect("/")

def logout(request):
    request.session.flush()  # clear session data
    return redirect("/")