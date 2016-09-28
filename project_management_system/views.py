from django.shortcuts import render
from forms import LoginForm, RegisterForm

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
    if request.method == "POST":
        form = RegisterForm(request.POST)
        form.is_valid()
        print "Register Submitted:", form.cleaned_data
    else:
        form = RegisterForm()
    return render(request, "register.html", { "form": form })

def instructor(request):
    context = {
            "professor_name": "Prof. John Smith",
            "projects" : [
                {
                    "project_name": "Space Race",
                    "project_description": "Lorem ipsum dolor sit amet, qualisque repudiare ut his, verear phaedrum disputando cu nec. \
                            Nonumy iisque est ne, cu quo graeco dissentias. Id adipisci accommodare sea. Debet suscipit in ius, ad laboramus\
                            gloriatur voluptaria qui. Sit alii habeo no, qui elitr constituto id."
                },
                {
                    "project_name": "Vim Package Manager",
                    "project_description": "Lorem ipsum dolor sit amet, qualisque repudiare ut his, verear phaedrum disputando cu nec. Nonumy\
                            iisque est ne, cu quo graeco dissentias. Id adipisci accommodare sea. Debet suscipit in ius, ad laboramus gloriatur\
                            voluptaria qui. Sit alii habeo no, qui elitr constituto id."
                }
                ],
            "inbox" : [
                {
                    "subject": "Message 1",
                    "body" : "Ad tation reprehendunt sit, ne eum autem dolor consectetuer. Ipsum diceret delenit vis ea, elitr maiestatis te ius.\
                            Menandri electram interesset in quo, odio ocurreret cu mea. At nec consul corpora, in illum debet vocent sea, in nec\
                            vivendo deterruisset."
                },
                {
                    "subject": "Message 2",
                    "body": "Veritus nominavi appareat at mel, vel commune scriptorem ea. Suscipit oportere ne vel. Ea appareat constituam definitiones\
                            mel. Nobis utinam prodesset ne usu, vis ut utroque facilis voluptua, ut tale assueverit nec. Sit novum mundi moderatius ut,\
                            cu prodesset definitionem has, mel te sonet principes."
                }
            ],
            "notifications" : [
                {
                    "subject": "Message 1",
                    "body" : "Ad tation reprehendunt sit, ne eum autem dolor consectetuer. Ipsum diceret delenit vis ea, elitr maiestatis te ius. Menandri\
                            electram interesset in quo, odio ocurreret cu mea. At nec consul corpora, in illum debet vocent sea, in nec vivendo deterruisset."
                },
                {
                    "subject": "Message 2",
                    "body": "Veritus nominavi appareat at mel, vel commune scriptorem ea. Suscipit oportere ne vel. Ea appareat constituam definitiones mel.\
                             Nobis utinam prodesset ne usu, vis ut utroque facilis voluptua, ut tale assueverit nec. Sit novum mundi moderatius ut, cu prodesset\
                             definitionem has, mel te sonet principes."
                }
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
    context = {
            "student_name": "Jeremy Corn",
            "projects" : [
                {
                    "project_name": "Space Race",
                    "project_description": "Lorem ipsum dolor sit amet, qualisque repudiare ut his, verear phaedrum disputando cu nec. \
                            Nonumy iisque est ne, cu quo graeco dissentias. Id adipisci accommodare sea. Debet suscipit in ius, ad laboramus\
                            gloriatur voluptaria qui. Sit alii habeo no, qui elitr constituto id."
                },
                {
                    "project_name": "Vim Package Manager",
                    "project_description": "Lorem ipsum dolor sit amet, qualisque repudiare ut his, verear phaedrum disputando cu nec. Nonumy\
                            iisque est ne, cu quo graeco dissentias. Id adipisci accommodare sea. Debet suscipit in ius, ad laboramus gloriatur\
                            voluptaria qui. Sit alii habeo no, qui elitr constituto id."
                }
                ],
            "inbox" : [
                {
                    "subject": "Message 1",
                    "body" : "Ad tation reprehendunt sit, ne eum autem dolor consectetuer. Ipsum diceret delenit vis ea, elitr maiestatis te ius.\
                            Menandri electram interesset in quo, odio ocurreret cu mea. At nec consul corpora, in illum debet vocent sea, in nec\
                            vivendo deterruisset."
                },
                {
                    "subject": "Message 2",
                    "body": "Veritus nominavi appareat at mel, vel commune scriptorem ea. Suscipit oportere ne vel. Ea appareat constituam definitiones\
                            mel. Nobis utinam prodesset ne usu, vis ut utroque facilis voluptua, ut tale assueverit nec. Sit novum mundi moderatius ut,\
                            cu prodesset definitionem has, mel te sonet principes."
                }
                ],
            "notifications" : [
                {
                    "subject": "Notification 1",
                    "body" : "Ad tation reprehendunt sit, ne eum autem dolor consectetuer. Ipsum diceret delenit vis ea, elitr maiestatis te ius. Menandri\
                            electram interesset in quo, odio ocurreret cu mea. At nec consul corpora, in illum debet vocent sea, in nec vivendo deterruisset."
                },
                {
                    "subject": "Notification 2",
                    "body": "Veritus nominavi appareat at mel, vel commune scriptorem ea. Suscipit oportere ne vel. Ea appareat constituam definitiones mel.\
                             Nobis utinam prodesset ne usu, vis ut utroque facilis voluptua, ut tale assueverit nec. Sit novum mundi moderatius ut, cu prodesset\
                             definitionem has, mel te sonet principes."
                }
                ]
            }
    return render(request, "student.html", context)

def projects(request):
    context = {
        "projects" : [
            {
                "project_name": "Space Race",
                "project_description": "Lorem ipsum dolor sit amet, qualisque repudiare ut his, verear phaedrum disputando cu nec. Nonumy iisque est ne, cu quo graeco dissentias. Id adipisci accommodare sea. Debet suscipit in ius, ad laboramus gloriatur voluptaria qui. Sit alii habeo no, qui elitr constituto id."
            },
            {
                "project_name": "Vim Package Manager",
                "project_description": "Lorem ipsum dolor sit amet, qualisque repudiare ut his, verear phaedrum disputando cu nec. Nonumy iisque est ne, cu quo graeco dissentias. Id adipisci accommodare sea. Debet suscipit in ius, ad laboramus gloriatur voluptaria qui. Sit alii habeo no, qui elitr constituto id."
            },
            {
                "project_name": "Space Race",
                "project_description": "Lorem ipsum dolor sit amet, qualisque repudiare ut his, verear phaedrum disputando cu nec. Nonumy iisque est ne, cu quo graeco dissentias. Id adipisci accommodare sea. Debet suscipit in ius, ad laboramus gloriatur voluptaria qui. Sit alii habeo no, qui elitr constituto id."
            },
            {
                "project_name": "Vim Package Manager",
                "project_description": "Lorem ipsum dolor sit amet, qualisque repudiare ut his, verear phaedrum disputando cu nec. Nonumy iisque est ne, cu quo graeco dissentias. Id adipisci accommodare sea. Debet suscipit in ius, ad laboramus gloriatur voluptaria qui. Sit alii habeo no, qui elitr constituto id."
            },
            {
                "project_name": "Space Race",
                "project_description": "Lorem ipsum dolor sit amet, qualisque repudiare ut his, verear phaedrum disputando cu nec. Nonumy iisque est ne, cu quo graeco dissentias. Id adipisci accommodare sea. Debet suscipit in ius, ad laboramus gloriatur voluptaria qui. Sit alii habeo no, qui elitr constituto id."
            },
            {
                "project_name": "Vim Package Manager",
                "project_description": "Lorem ipsum dolor sit amet, qualisque repudiare ut his, verear phaedrum disputando cu nec. Nonumy iisque est ne, cu quo graeco dissentias. Id adipisci accommodare sea. Debet suscipit in ius, ad laboramus gloriatur voluptaria qui. Sit alii habeo no, qui elitr constituto id."
            },
            {
                "project_name": "Space Race",
                "project_description": "Lorem ipsum dolor sit amet, qualisque repudiare ut his, verear phaedrum disputando cu nec. Nonumy iisque est ne, cu quo graeco dissentias. Id adipisci accommodare sea. Debet suscipit in ius, ad laboramus gloriatur voluptaria qui. Sit alii habeo no, qui elitr constituto id."
            },
            {
                "project_name": "Vim Package Manager",
                "project_description": "Lorem ipsum dolor sit amet, qualisque repudiare ut his, verear phaedrum disputando cu nec. Nonumy iisque est ne, cu quo graeco dissentias. Id adipisci accommodare sea. Debet suscipit in ius, ad laboramus gloriatur voluptaria qui. Sit alii habeo no, qui elitr constituto id."
            }
        ]
    }
    return render(request, "projects.html", context)
