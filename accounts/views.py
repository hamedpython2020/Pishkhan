import datetime
from datetime import date

from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from xhtml2pdf import pisa
from accounts.forms import EmployeeForm, ProjectForm, PayForm, SearchForm, NoteForm
from accounts.models import employee, project, payment
from works.models import Services


def index(request):
    employees = employee.objects.all()
    if request.method == 'POST' and request.user is not None:
        form = NoteForm(request.POST)
        user = request.user
        emp = employee.objects.get(user=user)
        emp.note = request.POST.get('note')
        emp.save()
        pass
    else:
        user = request.user
        if request.user.is_authenticated == True:
            user = request.user
            emp = employee.objects.get(user=user)
            form = NoteForm(initial={'note': emp.note})
        else:
            form = NoteForm()

    context = {
        'form': form,
        'employees': employees,
    }
    return render(request, 'accounts/index.html', context)


# Registration Page  ########


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
    return render(request, "accounts/login.html", context)


def Logout(request):
    logout(request)
    if request.GET.get('next'):
        return HttpResponseRedirect(request.GET.get('next'))
    return HttpResponseRedirect(reverse('accounts:login'))


# Model Page ##########
@login_required
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


@login_required
def Employee(request, employee_id):
    obj = employee.objects.get(pk=employee_id)
    context = {
        'obj': obj
    }
    return render(request, 'accounts/employee.html', context)

@login_required
def Newproject(request):
    if request.method == 'POST':
        project = ProjectForm(request.POST)
        if project.is_valid():
            newproj = project.save()
            return HttpResponseRedirect(reverse('accounts:project_list'))
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

@login_required
def NewPayment(request, project_id):
    today = date.today()
    if request.method == 'POST':
        pay = PayForm(request.POST)
        if pay.is_valid():
            pay.save()
            value = pay.cleaned_data['value']
            project = pay.cleaned_data['project']
            services = pay.cleaned_data['service']
            for i in range(0, len(pay.cleaned_data['service'])):
                service = pay.cleaned_data['service'][i]
                service.payed = True
                service.save()
            project.pay_service(value)
            project.save()
            return HttpResponseRedirect(reverse('accounts:payment_list'))
        context = {
            'pay': pay
        }
        pass
    else:
        pay = PayForm(initial={'project': project_id})
        pay.fields['service'].queryset = Services.objects.filter(project_id=project_id, payed=False)
        context = {
            'pay': pay,
            'today': today,
        }
    return render(request, 'accounts/payment.html', context)
@login_required
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
    pay.order_by('date').reverse()
    # services = pay.service.all()
    context = {
        'pay': pay,
        # 'services': services,
        'pay_c': pay_c,
        'search_box': search_box
    }
    return render(request, 'accounts/payment_list.html', context)
@login_required
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
@login_required
def pay_render_pdf(request, *args, **kwargs):
    pk = kwargs.get('pk')
    pay = get_object_or_404(payment, pk=pk)
    services = pay.service.all()
    # template_path = 'pay_render_pdf.html'
    context = {
        'pay': pay,
        'services': services,
        'date': datetime.date.today().strftime('%Y/%m/%d')
               }

    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template('accounts/pay_render_pdf.html')
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def delete_project(request, project_id):
    if request.method == 'POST':
        proj = project.objects.get(id=project_id)
        try:
            proj.delete()
            return HttpResponseRedirect(reverse('accounts:project_list'))
        except:
            context = {
                'error': 'شما نمیتوانید این پروژه را حذف کنید'
            }
            return render(request, 'accounts/project_delete.html', context)
    else:
        return render(request, 'accounts/project_delete.html',)
    pass

