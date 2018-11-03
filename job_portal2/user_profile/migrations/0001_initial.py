# Generated by Django 2.0.1 on 2018-09-21 12:21

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0002_auto_20180913_1115'),
    ]

    operations = [
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('creator', models.UUIDField(default=uuid.uuid4)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_modifier', models.UUIDField(default=uuid.uuid4)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('education_type', models.CharField(max_length=200)),
                ('course', models.CharField(max_length=200)),
                ('specialization', models.CharField(max_length=200)),
                ('board', models.CharField(max_length=200)),
                ('year_of_passing', models.IntegerField()),
                ('organization_name', models.CharField(max_length=200)),
                ('score_type', models.CharField(max_length=200)),
                ('score', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('creator', models.UUIDField(default=uuid.uuid4)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_modifier', models.UUIDField(default=uuid.uuid4)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('name', models.TextField()),
                ('url', models.URLField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('creator', models.UUIDField(default=uuid.uuid4)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_modifier', models.UUIDField(default=uuid.uuid4)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('user_type', models.CharField(choices=[('Seeker', 'Seeker'), ('Recruiter', 'Recruiter'), ('Representative', 'Representative'), ('Administrator', 'Administrator')], max_length=50)),
                ('description', models.CharField(max_length=100)),
                ('skills', models.ManyToManyField(to='core.Skill')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProfileAddress',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('creator', models.UUIDField(default=uuid.uuid4)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_modifier', models.UUIDField(default=uuid.uuid4)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Address')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_profile.Profile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('creator', models.UUIDField(default=uuid.uuid4)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_modifier', models.UUIDField(default=uuid.uuid4)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=250)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('description', models.TextField()),
                ('team_size', models.IntegerField()),
                ('role', models.CharField(max_length=250)),
                ('project_links', models.URLField()),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_profile.Profile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WorkExperience',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('creator', models.UUIDField(default=uuid.uuid4)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_modifier', models.UUIDField(default=uuid.uuid4)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('company_name', models.CharField(max_length=200)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('role', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_profile.Profile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='link',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_profile.Profile'),
        ),
        migrations.AddField(
            model_name='education',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_profile.Profile'),
        ),
    ]
