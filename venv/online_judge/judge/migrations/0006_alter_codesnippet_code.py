# Generated by Django 4.1.7 on 2023-04-06 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0005_alter_codesnippet_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codesnippet',
            name='code',
            field=models.CharField(max_length=1000),
        ),
    ]
