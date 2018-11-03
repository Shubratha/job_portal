from django.db import models
from core.models import AuditStamp, Skill, Address

USER_TYPE = (
    ('Seeker', 'Seeker'),
    ('Recruiter', 'Recruiter'),
    ('Representative', 'Representative'),
    ('Administrator', 'Administrator'),
)


class Profile(AuditStamp):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    skills = models.ManyToManyField(Skill)
    user_type = models.CharField(choices=USER_TYPE, max_length=50)
    description = models.CharField(max_length=100)


class Link(AuditStamp):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.TextField()
    url = models.URLField()


class Education(AuditStamp):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    education_type = models.CharField(max_length=200)
    course = models.CharField(max_length=200)
    specialization = models.CharField(max_length=200)
    board = models.CharField(max_length=200)
    year_of_passing = models.IntegerField()
    organization_name = models.CharField(max_length=200)
    score_type = models.CharField(max_length=200)
    score = models.DecimalField(max_digits=5, decimal_places=2)


class WorkExperience(AuditStamp):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    role = models.CharField(max_length=200)
    description = models.TextField()


class Project(AuditStamp):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    team_size = models.IntegerField()
    role = models.CharField(max_length=250)
    project_links = models.URLField()


class ProfileAddress(AuditStamp):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
