# Generated by Django 4.1.7 on 2023-02-24 14:18

from django.db import migrations
import django.utils.timezone
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_payment_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='date',
            field=django_jalali.db.models.jDateField(default=django.utils.timezone.now, verbose_name='تاریخ'),
        ),
    ]
