# Generated by Django 3.2 on 2025-07-04 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MentalCrowdWorkerProjectApp', '0003_basicinfo_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicinfo',
            name='name',
            field=models.CharField(max_length=100, verbose_name='사용자 이름'),
        ),
    ]
