from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from core.models import User, Student, Supervisor, Appointment


class StudentSignUpForm(UserCreationForm):
    courses = (
        ("CS" , "BSC (Computer Science)"),
        ("ACMP" , "BSC (Applied Computer Science)"),
    )
    first_name = forms.CharField(max_length=30, required=True, help_text="Optional")
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
    DAYS_OF_WEEK = (
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday'),
    )
    
    day = forms.ChoiceField(choices=DAYS_OF_WEEK)
    time = forms.TimeField()