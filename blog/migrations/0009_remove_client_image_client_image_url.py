# Generated by Django 5.1.1 on 2024-09-30 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_rename_update_account_updated_alter_client_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='image',
        ),
        migrations.AddField(
            model_name='client',
            name='image_url',
            field=models.URLField(blank=True),
        ),
    ]
