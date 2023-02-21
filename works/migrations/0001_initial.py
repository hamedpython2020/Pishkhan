# Generated by Django 4.1.7 on 2023-02-20 20:41

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import works.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('define_services', models.IntegerField(choices=[(1, 'درخواست پروانه'), (2, 'درخواست پایانکار'), (3, 'درخواست انتقال'), (4, 'درخواست تفکیکی'), (5, 'طراحی پلان'), (6, 'متفرقه')], verbose_name='خدمات تعریف شده')),
                ('cost_services', models.IntegerField(verbose_name='هزینه')),
                ('description', models.TextField(blank=True, verbose_name='خدمات متفرقه')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='تاریخ درخواست')),
                ('manager', models.CharField(max_length=50, verbose_name='مالک')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.project', verbose_name='پروژه')),
            ],
            options={
                'verbose_name': 'خدمات',
                'verbose_name_plural': 'خدمات',
            },
        ),
        migrations.CreateModel(
            name='p_document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(help_text='لطفا تمام فایل های خود را یک جا آپلود کنید', upload_to=works.models.p_document.user_directory_path, verbose_name='اسناد')),
                ('code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.project', verbose_name='پروژه')),
            ],
            options={
                'verbose_name': 'اسناد پروژه',
                'verbose_name_plural': 'اسناد پروژه',
            },
        ),
    ]