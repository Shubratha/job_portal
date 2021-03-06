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
            name='Company',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('creator', models.UUIDField(default=uuid.uuid4)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_modifier', models.UUIDField(default=uuid.uuid4)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('website', models.URLField()),
                ('size', models.IntegerField()),
                ('type', models.TextField(choices=[('PRIVATE', 'PRIVATE'), ('PUBLIC', 'PUBLIC')])),
                ('status', models.TextField(choices=[('ACTIVE', 'ACTIVE'), ('INACTIVE', 'INACTIVE')], default='ACTIVE')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CompanyAddress',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('creator', models.UUIDField(default=uuid.uuid4)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_modifier', models.UUIDField(default=uuid.uuid4)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='companyaddress', to='core.Address')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.Company')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CompanyRecruiter',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('creator', models.UUIDField(default=uuid.uuid4)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_modifier', models.UUIDField(default=uuid.uuid4)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.Company')),
                ('recruiter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_profile.Profile')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='companyrecruiter',
            unique_together={('company', 'recruiter')},
        ),
    ]
