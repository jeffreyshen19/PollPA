from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Poll

from .models import Profile

def index(request):
    return render(request, 'polls/index.html', {})

def poll(request, poll_id):
    return render(request, 'polls/poll.html', {
        "poll": {
            "poll_id": poll_id,
            "completed": True,
            "questions": [{
                "title": "Question 1 (Checkbox)?",
                "description": "Testing",
                "type": "checkbox",
                "options": [{
                    "title": "a",
                    "description": "This is a description."
                },
                {
                    "title": "b",
                    "description": ""
                },
                {
                    "title": "c",
                    "description": ""
                }]
            },
            {
                "title": "Question 2 (Radio)?",
                "description": "Testing",
                "type": "radio",
                "options": [{
                    "title": "a",
                    "description": ""
                },
                {
                    "title": "b",
                    "description": "This is a description"
                },
                {
                    "title": "c",
                    "description": ""
                }]
            }],
            "responses": [{
                "title": "Question 1 (Checkbox)?",
                "description": "Testing",
                "graph": "bar",
                "xlabel": "Options",
                "ylabel": "Values",
                "data": [{
                    "x": "a",
                    "y": 100
                },
                {
                    "x": "b",
                    "y": 45
                },
                {
                    "x": "c",
                    "y": 300
                }]
            },
            {
                "title": "Question 2 (Slider)?",
                "description": "Testing",
                "graph": "binary-slider",
                "data": {
                    "yes": 100,
                    "no": 50
                }
            }]
        }
    })

def _logout(request):
    logout(request)
    return redirect("index")

def _login(request):
    context = {
        "error": None
    }
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        # emails and usernames are _always_ the same
        username = request.POST.get('email', None)
        password = request.POST.get('password', None)
        if not username.endswith("@andover.edu"):
            username = username + "@andover.edu"
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            context["error"] = "Invalid username or password!"
    return render(request, 'polls/login.html', context)

def register(request):
    context = {
        "error": None
    }
    if request.method == "POST":
        try:
            username = request.POST.get('username', None)
            if not username.endswith("@andover.edu"):
                username = username + "@andover.edu"
            password = request.POST.get('password', None)
            grade = int(request.POST.get('grade', None))
            if grade > 2022 or grade < 2019:
                raise Exception()
            user = User.objects.create_user(username, username, password)
            Profile.objects.create(user=user, grade=grade)
            login(request, user)
            return redirect("index")
        except Exception as e:
            print(e)
            context["error"] = "Unable to create your account with the given information; please try again. Either your email is either registered, or you forgot to select a graduation year."
    return render(request, 'polls/register.html', context)

def reset(request):
    return render(request, 'polls/reset-password.html', {})

def account(request):
    return render(request, 'polls/account.html', {})

def suggest(request):
    return render(request, 'polls/suggest.html', {})
