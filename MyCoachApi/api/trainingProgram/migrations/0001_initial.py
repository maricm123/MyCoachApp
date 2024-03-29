# Generated by Django 4.2.4 on 2023-08-13 13:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0003_alter_coach_sport_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingProgram',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('pdf_file', models.FileField(blank=True, null=True, upload_to='pdfs/')),
                ('text', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('clients', models.ManyToManyField(blank=True, related_name='bought_programs', to='profiles.client')),
                ('coach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tweets', to='profiles.coach')),
                ('sport_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.sportcategory')),
            ],
        ),
    ]
