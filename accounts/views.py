import io
import os
from datetime import datetime, date
import cgi
from io import BytesIO, StringIO
from django.template import Context
from django.template.loader import get_template
from django.views.generic import ListView
from jalali_date import datetime2jalali, date2jalali
from django.views import View
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect, FileResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from xhtml2pdf import pisa
from accounts.forms import EmployeeForm, ProjectForm, NewUser, PayForm, SearchForm
from accounts.models import employee, project, payment
from works.models import Services


########## My functions ############
def my_view(request):
    jalali_join = datetime2jalali(request.user.date_joined).strftime('%y/%m/%d _ %H:%M:%S')
########### Home Page #############

def index(request):
    return render(request, 'accounts/index.html', context={})

######## Registration Page  ########


# def Signup(request):
#     if request.user is not None:
#         logout(request)
#         pass
#     if request.method == 'POST':
#         user = NewUser(request.POST)
#         if user.is_valid():
#             user = user.save()
#             login(request, user)
#             return HttpResponseRedirect(reverse('accounts:new_employee'))
#         context = {}
#     else:
#         user = NewUser()
#         context = {
#             'user': user
#         }
#     return render(request, 'accounts/signup.html', context)


def Login(request):
    if request.method == "GET":
        context = {
        }
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        # cap = request.POST.get('cap')
        # if cap == captcha_t:
        #     os.remove(path)
        #     status = 0
        user = authenticate(request, password=password, username=username)
        # givcap(1)
        if user is None:
            context = {
                'username': username,
                'error': 'موجود نیست'
            }

        else:
            login(request, user)
            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET.get('next'))
            else:
                return HttpResponseRedirect(reverse(viewname='index'))
            pass
        # else:
        #     os.remove(path)
        #     givcap()
        #     status = 0
        #     context = {
        #         'error': 'wrong captcha'
        #     }
        # pass
    return render(request, "accounts/login.html", context)


def Logout(request):
    logout(request)
    if request.GET.get('next'):
        return HttpResponseRedirect(request.GET.get('next'))
    return HttpResponseRedirect(reverse('accounts:login'))


########## Model Page ##########

def Newemployee(request):
    if request.user == None:
        return HttpResponseRedirect(reverse('login'))
    if request.method == 'POST':
        employee = EmployeeForm(request.POST, request.FILES)
        if employee.is_valid():
            data = employee.save(commit=False)
            data.user = request.user
            data.save()
            user = request.user
            user.is_staff = True
            user.save()
            return HttpResponseRedirect(reverse('index'))
            pass
    else:
        employee = EmployeeForm()
        context = {
            'employee': employee
        }
        return render(request, 'accounts/new_employee.html', context)


def Employee(request, employee_id):
    obj = employee.objects.get(pk=employee_id)
    context = {
        'obj': obj
    }
    return render(request, 'accounts/employee.html', context)


def Newproject(request):
    if request.method == 'POST':
        project = ProjectForm(request.POST)
        if project.is_valid():
            project.save()
            return HttpResponseRedirect(reverse('Newservice', current_app='works'))
    else:
        project = ProjectForm()
        context = {
            'project': project
        }
        return render(request, 'accounts/new_project.html', context)


def Projectlist(request):
    search_box = SearchForm(request.GET)
    objects = project.objects.all()
    if search_box.is_valid():
        if search_box.cleaned_data['code_p']:
            objects = objects.filter(code_p__contains=search_box.cleaned_data['code_p'])
        if search_box.cleaned_data['code_e']:
            objects = objects.filter(code_erg__contains=search_box.cleaned_data['code_e'])
        if search_box.cleaned_data['manger']:
            objects = objects.filter(manager__contains=search_box.cleaned_data['manger'])
    num = objects.count()
    context = {
        'objects': objects,
        'num': num,
        'search_box': search_box
    }
    return render(request, 'accounts/project_list.html', context)


def Project(request, project_id):
    obj = project.objects.get(pk=project_id)
    context = {
        'obj': obj
    }
    return render(request, 'accounts/project.html', context)


def NewPayment(request, project_id):
    today = date.today()
    if request.method == 'POST':
        pay = PayForm(request.POST)
        if pay.is_valid():
            pay.save()
            value = pay.value
            project = pay.project
            project.pay_service(value)
            project.save()
            return HttpResponseRedirect(reverse('accounts:payment_list'))
        context = {
            'pay': pay
        }
        pass
    else:
        pay = PayForm(initial={'project': project_id})
        context = {
            'pay': pay,
            'today': today,
        }
    return render(request, 'accounts/payment.html', context)


def Paymentlist(request):

    search_box = SearchForm(request.GET)
    pay = payment.objects.all().order_by('date')
    if search_box.is_valid():
        if search_box.cleaned_data['code_p']:
            pay = pay.filter(project__code_p__contains=search_box.cleaned_data['code_p'])
        if search_box.cleaned_data['manger']:
            pay = pay.filter(project__manager__contains=search_box.cleaned_data['manger'])
        if search_box.cleaned_data['min_value']:
            pay = pay.filter(value__gte=search_box.cleaned_data['min_value'])
        if search_box.cleaned_data['max_value']:
            pay = pay.filter(value__lte=search_box.cleaned_data['max_value'])
    pay_c = pay.count()
    context = {
        'pay': pay,
        'pay_c': pay_c,
        'search_box': search_box
    }
    return render(request, 'accounts/payment_list.html', context)


def Projectdetail(request, project_id):
    proj = project.objects.get(pk=project_id)
    pay = payment.objects.all()
    pay = pay.filter(project_id=project_id)
    pay_num = pay.count()
    service = Services.objects.all()
    service = service.filter(project_id=project_id)
    service_num = service.count()
    context = {
        'pay': pay,
        'project': proj,
        'pay_num': pay_num,
        'service': service,
        'service_num': service_num
    }
    return render(request, 'accounts/project_detail.html', context)

##############################################


def pay_render_pdf(request, pay_id):
    payments = get_object_or_404(payment, pk=pay_id)
    template_path = 'accounts/pay_pdf_view.html'
    context = {'payment': payments}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = ';filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


