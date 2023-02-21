from django.urls import path

from works import views

app_name = 'works'

urlpatterns = [
    path('services/new/', views.NewService, name='services_new'),
    path('services/list/', views.Servicelist, name='services_list'),
    path('documents/uplode/', views.Docupload, name='upload_doc')
]