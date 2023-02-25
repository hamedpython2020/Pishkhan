from django import forms
from django.contrib.auth.forms import UserCreationForm
from datetime import date, datetime

from django.utils import timezone

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
        widgets = {
            'date': forms.DateInput(attrs={'id': 'datepicker4'}),
        }
        pass

    # project = forms.ModelMultipleChoiceField(queryset=project.objects.all())
    def clean_date(self):
        pass

    # years = []
    # for i in range(1390, 1430):
    #     years.append(str(i))
    #     pass
    # months = {1: 'فروردین', 2: 'اردیبهشت', 3: 'خرداد',
    #           4: 'تیر', 5: 'مرداد', 6: 'شهریور',
    #           7: 'مهر', 8: 'آبان', 9: 'آذر',
    #           10: 'دی', 11: 'بهمن', 12: 'اسفند'
    #           }
    # date = forms.DateField(label='تاریخ', widget=forms.SelectDateWidget(years=years, months=months),
    #                        help_text='لطفا تاریخ را انتخاب کنید')

    # def clean_date(self):
    #     date = self.cleaned_data["date"]
    #
    #
    # pass


class ProjectForm(forms.ModelForm):
    class Meta:
        model = project
        exclude = []
        pass
    pass