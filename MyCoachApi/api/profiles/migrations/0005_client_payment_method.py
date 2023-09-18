# Generated by Django 4.2.4 on 2023-08-27 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0003_paymentmethod'),
        ('profiles', '0004_client_stripe_customer_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='payment_method',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='subscription.paymentmethod'),
        ),
    ]
