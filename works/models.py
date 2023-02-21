from django.db import models

# Create your models here.
from django.utils import timezone


class Services(models.Model):
    class Meta:
        verbose_name = 'خدمات'
        verbose_name_plural = 'خدمات'
    a_p = 1
    a_fw = 2
    a_tr = 3
    a_ta = 4
    dr_plan = 5
    another = 6
    services_choices = (
        (1, 'درخواست پروانه'),
        (2, 'درخواست پایانکار'),
        (3, 'درخواست انتقال'),
        (4, 'درخواست تفکیکی'),
        (5, 'طراحی پلان'),
        (6, 'متفرقه')
    )
    define_services = models.IntegerField("خدمات تعریف شده", choices=services_choices)
    cost_services = models.IntegerField('هزینه', null=False)
    description = models.TextField("خدمات متفرقه", blank=True)
    project = models.ForeignKey('accounts.project', verbose_name="پروژه", null=False, on_delete=models.PROTECT)
    date = models.DateField("تاریخ درخواست", default=timezone.now, null=False)

    def __str__(self):
        return "{1}-->{0}".format(self.project, self.define_services)
    pass


class p_document(models.Model):
    class Meta:
        verbose_name = "اسناد پروژه"
        verbose_name_plural = "اسناد پروژه"
        pass
    code = models.ForeignKey('accounts.project', verbose_name="پروژه", null=False, on_delete=models.CASCADE)
    def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'document/{0}'.format(instance.code, filename)

    file = models.FileField(verbose_name="اسناد", help_text="لطفا تمام فایل های خود را یک جا آپلود کنید", upload_to=user_directory_path)

    def __str__(self):
        return "document for {}".format(self.code)
    pass


