# Generated by Django 3.1.3 on 2020-11-08 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Testmania', '0004_questions_contest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questions',
            name='contest',
        ),
        migrations.RemoveField(
            model_name='questions',
            name='optionA',
        ),
        migrations.RemoveField(
            model_name='questions',
            name='optionB',
        ),
        migrations.RemoveField(
            model_name='questions',
            name='optionC',
        ),
        migrations.RemoveField(
            model_name='questions',
            name='optionD',
        ),
    ]
