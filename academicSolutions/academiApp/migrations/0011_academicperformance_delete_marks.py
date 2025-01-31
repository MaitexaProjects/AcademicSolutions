# Generated by Django 5.1.5 on 2025-01-31 02:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academiApp', '0010_marks'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicPerformance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks_obtained', models.DecimalField(decimal_places=2, max_digits=5)),
                ('grade', models.CharField(max_length=2)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academiApp.course')),
                ('student', models.ForeignKey(limit_choices_to={'role': 'student'}, on_delete=django.db.models.deletion.CASCADE, to='academiApp.academiapp')),
            ],
        ),
        migrations.DeleteModel(
            name='Marks',
        ),
    ]
