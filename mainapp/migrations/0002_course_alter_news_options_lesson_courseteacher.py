# Generated by Django 4.0.4 on 2022-06-02 17:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Edited')),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('description_as_markdown', models.BooleanField(default=False, verbose_name='As markdown')),
                ('cost', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Cost')),
                ('cover', models.CharField(default='no_image.svg', max_length=25, verbose_name='Cover')),
            ],
            options={
                'verbose_name': 'курс',
                'verbose_name_plural': 'курсы',
            },
        ),
        migrations.AlterModelOptions(
            name='news',
            options={'verbose_name': 'новость', 'verbose_name_plural': 'новости'},
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Edited')),
                ('deleted', models.BooleanField(default=False)),
                ('num', models.PositiveIntegerField(verbose_name='Lesson number')),
                ('title', models.CharField(max_length=256, verbose_name='Title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.course')),
            ],
            options={
                'ordering': ('course', 'num'),
            },
        ),
        migrations.CreateModel(
            name='CourseTeacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Edited')),
                ('deleted', models.BooleanField(default=False)),
                ('name_first', models.CharField(max_length=128, verbose_name='Name')),
                ('name_second', models.CharField(max_length=128, verbose_name='Surname')),
                ('day_birth', models.DateTimeField(verbose_name='Birth date')),
                ('course', models.ManyToManyField(to='mainapp.course')),
            ],
            options={
                'ordering': ('-created',),
                'abstract': False,
            },
        ),
    ]
