# Generated by Django 4.1.7 on 2023-02-23 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_rename_manager_payment_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='description',
            field=models.TextField(blank=True, verbose_name='بابت'),
        ),
    ]
