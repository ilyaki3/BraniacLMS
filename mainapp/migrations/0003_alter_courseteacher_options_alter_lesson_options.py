# Generated by Django 4.0.4 on 2022-06-02 17:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_course_alter_news_options_lesson_courseteacher'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='courseteacher',
            options={'verbose_name': 'учитель', 'verbose_name_plural': 'учителя'},
        ),
        migrations.AlterModelOptions(
            name='lesson',
            options={'ordering': ('course', 'num'), 'verbose_name': 'урок', 'verbose_name_plural': 'уроки'},
        ),
    ]
