from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "index.html")

def login(request):
    return render(request, "login.html")

def register(request):
    return render(request, "register.html")

def client(request):
    context = {
        "project_bids" : [
            { "team_name": "Team DU" },
            { "team_name": "Team Vim" }
        ]
    }
    return render(request, "client.html", context)
