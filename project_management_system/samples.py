sample_text = "Lorem ipsum dolor sit amet, qualisque repudiare ut his, verear phaedrum disputando cu nec. \
                Nonumy iisque est ne, cu quo graeco dissentias. Id adipisci accommodare sea. Debet suscipit in ius, ad laboramus\
                gloriatur voluptaria qui. Sit alii habeo no, qui elitr constituto id."

test_student = {
    "email": "student@du.com",
    "password": "password",
    "name": "Jeremy Corn",
    "projects" : [
        {
            "project_name": "Space Race",
            "project_description": sample_text
        },
        {
            "project_name": "Vim Package Manager",
            "project_description": sample_text
        }],
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
            "subject": "Notification 1",
            "body" : sample_text
        },
        {
            "subject": "Notification 2",
            "body": sample_text
        }]
}

test_instructor = {
    "email": "instructor@du.com",
    "password": "password",
    "name": "John Smith",
    "projects" : [
        {
            "project_name": "Space Race",
            "project_description": sample_text
        },
        {
            "project_name": "Vim Package Manager",
            "project_description": sample_text
        }],
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

test_projects = {
    "projects" : [
        {
            "project_name": "Space Race",
            "project_description": sample_text
        },
        {
            "project_name": "Vim Package Manager",
            "project_description": sample_text
        },
        {
            "project_name": "Space Race",
            "project_description": sample_text
        },
        {
            "project_name": "Vim Package Manager",
            "project_description": sample_text
        },
        {
            "project_name": "Space Race",
            "project_description": sample_text
        },
        {
            "project_name": "Vim Package Manager",
            "project_description": sample_text
        },
        {
            "project_name": "Space Race",
            "project_description": sample_text
        },
        {
            "project_name": "Vim Package Manager",
            "project_description": sample_text
        }
    ]
}

test_project = {
    "project_name": "Space Race",
    "project_description": sample_text,
    "project_reqs" : "Python, Ruby, Java, SQL",
    "project_tags": "fun, cool, interesting, tags"
}

