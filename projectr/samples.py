sample_text = "Lorem ipsum dolor sit amet, qualisque repudiare ut his, verear phaedrum disputando cu nec. \
                Nonumy iisque est ne, cu quo graeco dissentias. Id adipisci accommodare sea. Debet suscipit in ius, ad laboramus\
                gloriatur voluptaria qui. Sit alii habeo no, qui elitr constituto id."

test_messages = {
    "messages": [
        {
            "subject": "Re: Familiarity with C++",
            "body": "I think that I have enough knowledge in C++ to complete to project from CS 101 and CS 206.  What do you think?"
        },
        {
            "subject": "Time Constraints on my Project",
            "body": "Hi, I am a client for the Vim Package Manager but I need to project completed in one semester.  Is this possible?"
        },
        {
            "subject": "Difficulty of High Frequency Trading Engine Project",
            "body": "Hi, I am a potential client that wants the students to make a high frequency trading engine that will make billions of dollars.  I am not sure if the project is outside of the scope of your course though.  Let me know"
        }]
}

test_projects = {
    "projects" : [
        {
            "project_name": "Space Race",
            "project_description": "It's a race to the finish by some of NASAs top astronauts. Race throughout space and time in a thrilling video game written in C++"
        },
        {
            "project_name": "Vim Package Manager",
            "project_description": "A project to make installing and managing vim plugins simple and painless"
        },
        {
            "project_name": "Emacs Plugin to do Regex",
            "project_description": "Adding a simple plugin to Emacs that makes a simple feature possible without getting carpel tunnel.",
        },
        {
            "project_name": "High Frequency Trading Engine in JavaScript",
            "project_description": "Everybody uses C++ for their HFT engines, but JavaScript is the future of low latency applications, and this project will make billions of dollars."
        },
        {
            "project_name": "Optimizing compiler",
            "project_description": "GCC needs to be garbage collected: its trash.  I am looking to replace it with a much better optimizing compiler based on the LLWM framework."
        }
    ]
}

test_student = {
    "email": "student@du.com",
    "password": "password",
    "name": "Jeremy Corn",
    "projects" : test_projects["projects"][:2],
    "inbox" : [
        {
            "subject": "Message 1",
            "body" : sample_text
        },
        {
            "subject": "Message 2",
            "body": sample_text
        }],
    "notifications" : [
        {
            "subject": "Submitted Bid",
            "body" : "You have submitted a bid on the Vim Package Manager project."
        }]
}

test_instructor = {
    "email": "instructor@du.com",
    "password": "password",
    "name": "John Smith",
    "projects" : [
        {
            "project_name": "Space Race",
            "project_description": "We are a great fit for this project because we have been to space.  While we were in space, we wrote a C++ application with rocket ships racing each other.  Our experience is great, and we are ready to blast off on this project.",
            "biddee_names": ["Devin Johnston", "Robert Guthrie"]
        },
        {
            "project_name": "Vim Package Manager",
            "project_description": "We are a team of dedicated vim plugin developers who would like to also develop a vim package manager.  Our personal vim plugins have millions of users.  Jeremy's first word was Vi and Tim's was hjkl.",
            "biddee_names": ["Tim Pope", "Jeremy Dorne"]
        }],
    "inbox" : test_messages["messages"],
    "notifications" : [
        {
            "subject": "Message 1",
            "body" : sample_text
        },
        {
            "subject": "Message 2",
            "body": sample_text
        }]
}

test_client = {
    "email": "client@du.com",
    "password": "password",
    "name": "Rick Hong, Ph.D",
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


test_project = {
    "project_name": "Space Race",
    "project_description": "It's a race to the finish by some of NASAs top astronauts. Race throughout space and time in a thrilling video game written in C++",
    "project_reqs" : "C++, Gamedev, SQL",
    "project_tags": "C++, space, game",
    "client_email": "client@du.com"
}


