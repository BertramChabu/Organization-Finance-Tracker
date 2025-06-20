# Generated by Django 5.2.1 on 2025-06-17 08:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='academicyear',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='school',
            name='capacity',
        ),
        migrations.RemoveField(
            model_name='school',
            name='category',
        ),
        migrations.AlterField(
            model_name='school',
            name='established_year',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='school',
            name='principal',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='school_principal', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='school',
            name='school_type',
            field=models.CharField(choices=[('public', 'Public'), ('private', 'Private'), ('church', 'Church')], max_length=20),
        ),
    ]
