# Generated by Django 3.2.6 on 2021-08-11 13:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_customer_mobile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='mobile',
        ),
    ]
