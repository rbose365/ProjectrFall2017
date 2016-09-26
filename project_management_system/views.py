from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "index.html")

def login(request):
    return render(request, "login.html")

def register(request):
    return render(request, "register.html")

def instructor(request):
    context = {
            "notifications" : [
                { "notification_content": "Notification 1" },
                { "notification_content": "Notification 2" }
            ],
            "messages" : [
                { "message_content": "Message 1" },
                { "message_content": "Message 2" }
            ],
            "project_bids" : [
                { "team_name": "Team DU" },
                { "team_name": "Team Vim" }
            ]
        }
    return render(request, "instructor.html", context)

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
