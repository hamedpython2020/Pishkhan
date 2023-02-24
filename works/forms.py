from django import forms

from works.models import p_document, Services


class ServicesForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'id': 'datepicker4'}),
        }
    pass



class DocForm(forms.ModelForm):
    class Meta:
        model = p_document
        exclude = []
        pass
    pass
