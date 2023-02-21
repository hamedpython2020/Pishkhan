from django import forms

from works.models import p_document, Services


class ServicesForm(forms.ModelForm):
    class Meta:
        model = Services
        exclude = []
        pass
    # years = []
    # for i in range(1330, 1420):
    #     years.append(str(i))
    #     pass
    # months = {1: 'فروردین', 2: 'اردیبهشت', 3: 'خرداد',
    #           4: 'تیر', 5: 'مرداد', 6: 'شهریور',
    #           7: 'مهر', 8: 'آبان', 9: 'آذر',
    #           10: 'دی', 11: 'بهمن', 12: 'اسفند'
    #           }
    # date = forms.DateField(label="تاریخ ثبت", widget=forms.SelectDateWidget(years, months))
    pass



class DocForm(forms.ModelForm):
    class Meta:
        model = p_document
        exclude = []
        pass
    pass
