from PIL.ImagePath import Path
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from accounts.forms import EmployeeForm, ProjectForm, NewUser, PayForm
from accounts.models import employee, project, payment


########### Home Page #############

def index(request):
    return render(request, 'accounts/index.html', context={})

######## Registration Page  ########


def Signup(request):
    if request.user is not None:
        logout(request)
        pass
    if request.method == 'POST':
        user = NewUser(request.POST)
        if user.is_valid():
            user = user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('accounts:new_employee'))
        context = {}
    else:
        user = NewUser()
        context = {
            'user': user
        }
    return render(request, 'accounts/signup.html', context)


def Login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, password=password, username=username)
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
        pass
    else:
        context = {}
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
    objects = project.objects.all()
    num = objects.count()
    context = {
        'objects': objects,
        'num': num
    }
    return render(request, 'accounts/payment_list.html', context)


def Project(request, project_id):
    obj = project.objects.get(pk=project_id)
    context = {
        'obj': obj
    }
    return render(request, 'accounts/project.html', context)


def NewPayment(request):
    if request.method == 'POST':
        pay = PayForm(request.POST)
        if pay.is_valid():
            pay = pay.save()
            value = pay.value
            customer = pay.manager
            customer.pay_service(value)
            customer.save()
            pay.save()
            return HttpResponseRedirect(reverse('accounts:payment_list'))
        context = {

        }
        pass
    else:
        pay = PayForm()
        context = {
            'pay': pay
        }
    return render(request, 'accounts/payment.html', context)


def Paymentlist(request):
    try:
        pay = payment.objects.all().order_by('date')
        pay_c = pay.count()
        context = {
            'pay': pay,
            'pay_c': pay_c
        }
    except:
        error = 'Something is wrong'
        context = {
            'error': error
        }
        pass
    return render(request, 'accounts/payment_list.html', context)
