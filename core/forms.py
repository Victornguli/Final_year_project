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
        required=True, help_text="Optional",
        widget=forms.TextInput(
            attrs={
                'class': 'bg-red',
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

# class CreateAppointmentForm(forms.ModelForm):
#     time = forms.DateTimeField()
    
#     class Meta:
#         model = Appointment
#         fields = ("time",)
    
#     @transaction.atomic
#     def save(self):
#         #user = request.user
#         appointment = Appointment.objects.create(time=self.cleaned_data.get("time"))
#         return appointment

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

# class DocumentForm(forms.ModelForm):
#     document = forms.FileField()
#     class Meta:
#         model = Document
#         fields = ('document', )

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50, required=True)
    document = forms.FileField()