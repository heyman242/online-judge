# Generated by Django 4.1.7 on 2023-04-07 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0007_alter_codesnippet_code_test_cases'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test_cases',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='judge.questions'),
        ),
    ]
