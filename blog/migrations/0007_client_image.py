# Generated by Django 5.1.1 on 2024-09-30 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_account_account_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='clients/'),
        ),
    ]
