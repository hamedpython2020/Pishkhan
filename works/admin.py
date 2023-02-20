from django.contrib import admin

# Register your models here.
from works.models import Services, p_document

admin.site.register(Services)
admin.site.register(p_document)