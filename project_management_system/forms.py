from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

class RegisterForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    user_type = forms.ChoiceField(widget=forms.RadioSelect, label="User Type",
                    choices=[("S", "Student"), ("I", "Instructor"), ("C", "Client")])

class ProjectSubmissionForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput, label="Project Name")
    requirements = forms.CharField(widget=forms.TextInput, label="Project Requirements")
    keywords = forms.CharField(widget=forms.TextInput, label="Keywords")
    description = forms.CharField(widget=forms.TextInput, label="Description")

class MessageForm(forms.Form):
    recipient = forms.CharField(widget=forms.TextInput, label="To")
    text = forms.CharField(widget=forms.Textarea, label="Message Text")

class BidSubmissionForm(forms.Form):
    team_members = forms.CharField(widget=forms.TextInput, label="Team Members")
    description = forms.CharField(widget=forms.Textarea, label="Note to Instructors/Client")
