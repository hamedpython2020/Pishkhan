from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import employee, payment, project


class NewUser(UserCreationForm):
    pass


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = employee
        exclude = ['user']
        pass
    pass


class PayForm(forms.ModelForm):
    class Meta:
        model = payment
        exclude = []
        pass
    pass


class ProjectForm(forms.ModelForm):
    class Meta:
        model = project
        exclude = []
        pass
    pass