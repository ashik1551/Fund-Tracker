# Generated by Django 5.0.6 on 2024-05-29 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_expense_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='income',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
