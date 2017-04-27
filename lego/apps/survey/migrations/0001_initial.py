# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-30 17:12
from __future__ import unicode_literals

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Alternative',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('deleted', models.BooleanField(default=False, editable=False)),
                ('alternative_text', models.TextField(max_length=255)),
                ('alternative_type', models.CharField(choices=[(1, 'radio_button'), (2, 'check_box'), (3, 'text_box')], default=1, max_length=20)),
                ('created_by', models.ForeignKey(default=None, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='alternative_created', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'default_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('deleted', models.BooleanField(default=False, editable=False)),
                ('answer_text', models.TextField(blank=True, max_length=255)),
                ('alternative', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='survey.Alternative')),
                ('created_by', models.ForeignKey(default=None, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answer_created', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'default_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('deleted', models.BooleanField(default=False, editable=False)),
                ('question_type', models.CharField(choices=[(1, 'single_choice'), (2, 'multiple_choice'), (3, 'text_field')], max_length=20)),
                ('question_text', models.TextField(max_length=255)),
                ('mandatory', models.BooleanField(default=False)),
                ('relative_index', models.IntegerField(null=True)),
                ('created_by', models.ForeignKey(default=None, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='question_created', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['relative_index'],
            },
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('deleted', models.BooleanField(default=False, editable=False)),
                ('submitted_time', models.DateTimeField(null=True)),
                ('submitted', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(default=None, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submission_created', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'default_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('deleted', models.BooleanField(default=False, editable=False)),
                ('title', models.CharField(max_length=100)),
                ('active_from', models.DateTimeField(default=django.utils.timezone.now)),
                ('template_type', models.CharField(blank=True, choices=[('company_presentation', 'company_presentation'), ('lunch_presentation', 'lunch_presentation'), ('course', 'course'), ('kid_event', 'kid_event'), ('party', 'party'), ('social', 'social'), ('other', 'other'), ('event', 'event')], max_length=30, null=True)),
                ('created_by', models.ForeignKey(default=None, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='survey_created', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(default=None, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='survey_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'default_manager_name': 'objects',
            },
        ),
        migrations.AddField(
            model_name='submission',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='survey.Survey'),
        ),
        migrations.AddField(
            model_name='submission',
            name='updated_by',
            field=models.ForeignKey(default=None, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submission_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='submission',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='surveys', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='question',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='survey.Survey'),
        ),
        migrations.AddField(
            model_name='question',
            name='updated_by',
            field=models.ForeignKey(default=None, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='question_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='answer',
            name='submission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='survey.Submission'),
        ),
        migrations.AddField(
            model_name='answer',
            name='updated_by',
            field=models.ForeignKey(default=None, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answer_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='alternative',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alternatives', to='survey.Question'),
        ),
        migrations.AddField(
            model_name='alternative',
            name='updated_by',
            field=models.ForeignKey(default=None, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='alternative_updated', to=settings.AUTH_USER_MODEL),
        ),
    ]