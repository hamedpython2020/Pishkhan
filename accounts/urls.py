from django.urls import path

from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('employee/new/', views.Newemployee, name='new_employee'),
    path('employee/<int:employee_id>/', views.Employee, name='employee'),
    path('payment/<int:project_id>/new/', views.NewPayment, name='new_payment'),
    path('payment/list/', views.Paymentlist, name='payment_list'),
    # path('signup/', views.Signup, name='signup'),
    path('project/new/', views.Newproject, name='project_new'),
    path('project/list/', views.Projectlist, name='project_list'),
    path('project/<int:project_id>/', views.Project, name='project'),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
]
