# Generated by Django 4.2.3 on 2023-09-24 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_alter_customer_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(help_text='Digite o nome do cliente', max_length=255, unique=True),
        ),
    ]