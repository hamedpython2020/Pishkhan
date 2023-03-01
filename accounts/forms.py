from django import forms
from django.contrib.auth.forms import UserCreationForm
from datetime import date, datetime

from django.utils import timezone

from accounts.models import employee, payment, project
from works.models import Services


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
        widgets = {
            'date': forms.DateInput(attrs={'id': 'datepicker4'}),
        }
        pass

    service = forms.ModelMultipleChoiceField(queryset=Services.objects.all())



class ProjectForm(forms.ModelForm):
    class Meta:
        model = project
        exclude = []
        pass
    pass


class SearchForm(forms.Form):
    manger = forms.CharField(label='نام مالک', min_length=3, required=False)
    code_p = forms.CharField(label="کد نوسازی", help_text='لطفا کد نوسازی را با شکل (0-0-0-0-0) وارد کنبد', required=False)
    code_e = forms.CharField(label="کد ارجاع", help_text='لطفا کد ارجاع را وارد کنبد', required=False)
    min_value = forms.IntegerField(label="حداقل مبلغ", required=False)
    max_value = forms.IntegerField(label="حداکثز مبلغ", required=False)
    construction = 7
    land = 8
    project_finish = 9
    loading_beam = 6
    columnarization = 5
    Destruction = 1
    Foundation_concreting = 4
    Excavation = 2
    foundation = 3
    status_choices = (
        (1, 'تخریب'),
        (2, 'گودبرداری'),
        (3, 'چینش فندانسیون'),
        (4, 'بتن ریزی فندانسیون'),
        (5, 'ستون ریزی'),
        (6, 'تیر ریزی'),
        (7, 'درحال ساخت'),
        (8, 'زمین خالی'),
        (9, 'متفرقه')
    )
    status = forms.ChoiceField(label='وضعیت پروژه', choices=status_choices, required=False)

    pass


