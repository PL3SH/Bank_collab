# Generated by Django 5.1.1 on 2025-02-19 01:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_appointment'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('PENDING', 'Pendiente'), ('SENT', 'Enviado'), ('FAILED', 'Fallido'), ('DRAFT', 'Borrador')], default='DRAFT', max_length=10)),
                ('priority', models.CharField(choices=[('HIGH', 'Alta'), ('MEDIUM', 'Media'), ('LOW', 'Baja')], default='MEDIUM', max_length=6)),
                ('scheduled_for', models.DateTimeField(blank=True, null=True)),
                ('sent_at', models.DateTimeField(blank=True, null=True)),
                ('error_message', models.TextField(blank=True, null=True)),
                ('template_used', models.CharField(blank=True, max_length=100)),
                ('attachments', models.FileField(blank=True, null=True, upload_to='email_attachments/')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='email_notifications', to='blog.client')),
            ],
            options={
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['status', 'priority'], name='blog_emailn_status_8fa4ce_idx'), models.Index(fields=['recipient', '-created_at'], name='blog_emailn_recipie_5e4387_idx')],
            },
        ),
    ]
