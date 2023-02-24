from django.contrib.auth.models import User
from django.db import models
from django_jalali.db import models as jmodels

# Create your models here.
from django.utils import timezone


class employee(models.Model):
    class Mete:
        verbose_name = "کارمند"
        verbose_name_plural = "کارمند"
        pass

    user = models.OneToOneField(User, verbose_name="کاربر", on_delete=models.CASCADE, null=False)
    id_code = models.CharField("کدملی", null=False, blank=False, max_length=10, default=1010)
    l_name = models.CharField("نام خانوادگی", max_length=30, null=False, auto_created=False)
    join_time = models.DateTimeField("زمان عضویت", auto_now_add=True)

    def user_directory_path(instance, filename):
        return 'user/employees/{0}_{1}'.format(instance.id_code, filename)
    picture = models.ImageField("تصویر", upload_to=user_directory_path, null=True,
                                help_text="لطفا یک عکس با  فامیل خود آپلود کنید")

    def __str__(self):
        return "{}".format(self.l_name)
    pass



class project(models.Model):
    class Meta:
        verbose_name = 'پروژه'
        verbose_name_plural = 'پروژه'

    code_p = models.CharField("کد نوسازی", null=False, default='0-0-0-0-0-0', max_length=50)
    code_erg = models.CharField("کد ارجاع", null=False, default='0', max_length=50)
    add_time = models.DateTimeField('زمان ثبت', auto_now_add=True)
    bill = models.IntegerField('صورتحساب', null=False, default=0)
    construction = 7
    land = 8
    project_finish = 9
    loading_beam = 6
    columnarization = 5
    Destruction = 1
    Foundation_concreting = 4
    Excavation = 2
    foundation = 3
    status_choices = (
        (1, 'تخریب'),
        (2, 'گودبرداری'),
        (3, 'چینش فندانسیون'),
        (4, 'بتن ریزی فندانسیون'),
        (5, 'ستون ریزی'),
        (6, 'تیر ریزی'),
        (7, 'درحال ساخت'),
        (8, 'زمین خالی'),
        (9, 'متفرقه')
    )
    status = models.IntegerField('وضعیت پروژه', choices=status_choices)
    description = models.TextField(verbose_name="توضیحات", blank=True)
    manager = models.CharField("سازنده", null=False, max_length=50)

    def __str__(self):
        return self.code_p

    def pay_service(self, amount):
        self.bill -= amount
        self.save()
        return self

    def spend(self, value):
        self.bill += value
        self.save()
        return self
    pass




class payment(models.Model):
    class Meta:
        verbose_name = 'پرداخت'
        verbose_name_plural = 'پرداخت'
        pass
    project = models.ForeignKey('project', verbose_name="کد نوسازی", on_delete=models.PROTECT, null=False)
    value = models.IntegerField('مبلغ', null=False, default=0)
    date = models.DateField("تاریخ", null=False, default=timezone.now)
    description = models.TextField(verbose_name="بابت", blank=True)

    def __str__(self):
        return "{} --> {}".format(self.project, self.value)
    pass
