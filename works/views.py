from datetime import date

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from accounts.forms import SearchForm
from accounts.models import project
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


def NewService(request, project_id):
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
        context = {
         'service': service
        }
    else:
        proj = project.objects.get(pk=project_id)
        service = ServicesForm(initial={'project': project_id})
        context = {
            'service': service,
            'today': date.today()
        }
    return render(request, 'works/service_new.html', context)


def Servicelist(request):
    search_box = SearchForm(request.GET)
    service = Services.objects.all().order_by('date')
    if search_box.is_valid():
        if search_box.cleaned_data['code_p']:
            service = service.filter(project__code_p__contains=search_box.cleaned_data['code_p'])
        if search_box.cleaned_data['manger']:
            service = service.filter(project__manager__contains=search_box.cleaned_data['manger'])
    service_c = service.count()
    context = {
        'service': service,
        'service_c': service_c,
        'search_box': search_box
    }
    return render(request, 'works/service_list.html', context)
