# Generated by Django 4.1.7 on 2023-04-10 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0008_alter_test_cases_question'),
    ]

    operations = [
        migrations.RenameField(
            model_name='test_cases',
            old_name='inputs',
            new_name='case',
        ),
        migrations.RemoveField(
            model_name='test_cases',
            name='outputs',
        ),
    ]
