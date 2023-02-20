from django.contrib import admin

# Register your models here.
from accounts.models import employee, project, payment

admin.site.register(employee)
admin.site.register(project)
admin.site.register(payment)