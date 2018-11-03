# Generated by Django 2.0.1 on 2018-09-24 07:20

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('creator', models.UUIDField(default=uuid.uuid4)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_modifier', models.UUIDField(default=uuid.uuid4)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('SHORTLISTED', 'SHORTLISTED'), ('JOB OFFERED', 'JOB OFFERED'), ('RECRUITED', 'RECRUITED'), ('OFFER_REJECTED', 'OFFER_REJECTED'), ('CANDIDATE_REJECTED', 'CANDIDATE_REJECTED')], default='APPLIED', max_length=30)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_profile.Profile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='JobPosting',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_modifier', models.UUIDField(default=uuid.uuid4)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('creator', models.UUIDField(editable=False)),
                ('title', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('FULL_TIME', 'FULL TIME'), ('PART_TIME', 'PART TIME'), ('INTERNSHIP', 'INTERNSHIP'), ('CONTRACT', 'CONTRACT'), ('FREELANCE', 'FREELANCE')], max_length=50)),
                ('category', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('min_experience', models.IntegerField()),
                ('max_experience', models.IntegerField()),
                ('vacancies', models.IntegerField()),
                ('status', models.CharField(choices=[('INITIAL', 'INITIAL'), ('WAITING FOR APPROVAL', 'WAITING FOR APPROVAL'), ('POSTED', 'POSTED'), ('HOLD', 'HOLD'), ('EXPIRED', 'EXPIRED')], max_length=30)),
                ('company', models.CharField(max_length=200)),
                ('skills', models.ManyToManyField(to='core.Skill')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='jobapplication',
            name='jobPosting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job_posting.JobPosting'),
        ),
    ]