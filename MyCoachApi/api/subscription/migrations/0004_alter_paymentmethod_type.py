# Generated by Django 4.2.4 on 2023-08-27 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0003_paymentmethod'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentmethod',
            name='type',
            field=models.CharField(default='card', max_length=50),
        ),
    ]
