from django.contrib import admin
from django.contrib import admin
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin


# Register your models here.
from accounts.models import employee, project, payment

admin.site.register(employee)
admin.site.register(project)
admin.site.register(payment)

class MyInlines1(TabularInlineJalaliMixin, admin.TabularInline):
    model = payment
