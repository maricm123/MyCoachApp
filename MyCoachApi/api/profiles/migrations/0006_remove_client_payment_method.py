# Generated by Django 4.2.4 on 2023-09-28 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_client_payment_method'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='payment_method',
        ),
    ]
