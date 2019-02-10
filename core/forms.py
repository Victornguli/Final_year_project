from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from core.models import User, Student, Supervisor


class StudentSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text="Optional")
    last_name = forms.CharField(max_length=30, required=True, help_text="Optional")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        # student.interests.add(*self.cleaned_data.get('interests'))
        return user

class SupervisorSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_supervisor = True
        user.save()
        supervisor = Supervisor.objects.create(user=user)
        return user