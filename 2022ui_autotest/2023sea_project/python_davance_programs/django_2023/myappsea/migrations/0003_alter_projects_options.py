# Generated by Django 4.1.4 on 2024-01-13 08:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myappsea', '0002_rename_ids_projects_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projects',
            options={'managed': True, 'verbose_name': '项目表', 'verbose_name_plural': '项目表'},
        ),
    ]