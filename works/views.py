from datetime import date

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from works.forms import DocForm, ServicesForm
from works.models import Services


def Docupload(request):
    if request.method == 'POST':
        document = DocForm(request.POST, request.FILES)
        if document.is_valid():
            document.save()
            return HttpResponseRedirect(reverse('index'))
        context = {}
        pass
    else:
        document = DocForm()
        context = {
            'document': document
        }
    return render(request, 'works/upload_doc.html', context)


def NewService(request):
    if request.method == 'POST':
        service = ServicesForm(request.POST, request.FILES)
        if service.is_valid():
            res = service.save(commit=False)
            today = service.cleaned_data['date']
            res.date = today
            res.save()
            cost_service = res.cost_services
            projects = res.project
            projects.spend(cost_service)
            projects.save()
            return HttpResponseRedirect(reverse('works:services_list'))
        else:
            context = {
                'error': 'Something went wrong'
            }
    else:
        service = ServicesForm()
        context = {
            'service': service,
            'today': date.today()
        }
    return render(request, 'works/service_new.html', context)


def Servicelist(request):
     service = Services.objects.all().order_by('date')
     service_c = service.count()
     context = {
         'service': service,
         'service_c': service_c
     }
     return render(request, 'works/service_list.html', context)
