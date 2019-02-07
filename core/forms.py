from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from core.models import User, Student, Supervisor


class StudentSignUpForm(UserCreationForm):
    # interests = forms.ModelMultipleChoiceField(
    #     queryset=Subject.objects.all(),widget=forms.CheckboxSelectMultiple,required=True)

    class Meta(UserCreationForm.Meta):
        model = User

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