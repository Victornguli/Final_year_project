from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from core.models import *


class StudentSignUpForm(UserCreationForm):
    courses = (
        ("CS" , "BSC (Computer Science)"),
        ("ACMP" , "BSC (Applied Computer Science)"),
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        help_text="Optional",
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Write your name here'
                }
            )
        )
    last_name = forms.CharField(max_length=30, required=True, help_text="Optional")
    registration_number = forms.CharField(max_length=30, required=True,help_text="Required")
    course = forms.ChoiceField(help_text="Required", choices=courses)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2","registration_number","course")

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user, first_name=user.first_name,last_name=user.last_name, email=user.email, reg_number=self.cleaned_data.get("registration_number"), course=self.cleaned_data.get("course"))

        # student.interests.add(*self.cleaned_data.get('interests'))
        return user

class SupervisorSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text="Optional")
    last_name = forms.CharField(max_length=30, required=True, help_text="Optional")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_supervisor = True
        user.save()
        supervisor = Supervisor.objects.create(user=user, first_name=user.first_name, last_name=user.last_name, email=user.email)
        return user

class CreateAppointmentForm(forms.Form):
    date = forms.DateField()
    time = forms.DateTimeField(widget = forms.DateTimeInput)

class SelectAvailableDaysForm(forms.Form):
    monday = forms.TimeField(required=False)
    tuesday = forms.TimeField(required=False)
    wednesday = forms.TimeField(required=False)
    thursday = forms.TimeField(required=False)
    friday = forms.TimeField(required=False)
    saturday = forms.TimeField(required=False)
    sunday = forms.TimeField(required=False)

class SetScheduleForm(forms.Form):
    start_date = forms.DateField(required="False")
    end_date = forms.DateField(required="False")

class SetMilestoneForm(forms.Form):
    milestone = forms.CharField()
    start_date = forms.DateField(required="False")
    end_date = forms.DateField(required="False")

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50, required=True)
    document = forms.FileField()

class CreateProjectForm(forms.Form):
    title = forms.CharField(max_length=50, required=True, help_text="Enter your Project Title")
    abstract = forms.CharField(
        widget= forms.Textarea(
            attrs={
                "placeholder":"Type in your project abstract here"
            }
        ),
        min_length=200, max_length=1000, required=True,
        help_text="Your abstract should be more than 200 words"
    )
    abstract_document = forms.FileField(help_text="Upload your abstract document in a doc or docx format")

class SendCommentForm(forms.Form):
    comment = forms.CharField(
        max_length=200,
        initial = "Asas",
        widget=forms.Textarea(
            attrs={
                "rows":"5",
                "cols":"30",
                "placeholder":"Add your comment here",
            }
        ),
    )

class UpdateProfileForm(forms.Form):
    user = User
    first_name = forms.CharField(
        initial = "supervisor",
        max_length=50,
        widget = forms.TextInput(
        )
        )
    last_name = forms.CharField(max_length=50)
    user_name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50)
