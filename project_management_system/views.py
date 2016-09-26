from django.shortcuts import render
from forms import LoginForm

# Create your views here.
def index(request):
    return render(request, "index.html")

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        form.is_valid()
        print "Login Sumbitted:", form.cleaned_data
    else:
        form = LoginForm()
    return render(request, "login.html", { "form": form })

def register(request):
    return render(request, "register.html")

def instructor(request):
    return render(request, "instructor.html")

def client(request):
    context = {
            "project_bids" : [
                { 
                    "team_name": "Team DU",
                    "project_name": "Space Race",
                    "team_member_names": ["Robby Guthrie", "Devin Johnston"]
                },
                { 
                    "team_name": "Team Vim",
                    "project_name": "Vim Package Manager",
                    "team_member_names": ["Tim Pope", "Jeremy Dorne"]
                }
            ]
    }
    return render(request, "client.html", context)

def student(request):
    return render(request, "student.html")
