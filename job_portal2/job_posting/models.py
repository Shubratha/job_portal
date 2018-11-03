from django.db import models
from core.models import AuditStamp, Skill
from user_profile.models import Profile

JOB_TYPE = (
    ('FULL_TIME', 'FULL TIME'),
    ('PART_TIME', 'PART TIME'),
    ('INTERNSHIP', 'INTERNSHIP'),
    ('CONTRACT', 'CONTRACT'),
    ('FREELANCE', 'FREELANCE'),
)

JOB_POSTING_STATUS = (
    ('INITIAL', 'INITIAL'),
    ('WAITING FOR APPROVAL', 'WAITING FOR APPROVAL'),
    ('POSTED', 'POSTED'),
    ('HOLD', 'HOLD'),
    ('EXPIRED', 'EXPIRED')
)


JOB_APPLICATION_STATUS = (
    ('SHORTLISTED', 'SHORTLISTED'),
    ('JOB OFFERED', 'JOB OFFERED'),
    ('RECRUITED', 'RECRUITED'),
    ('OFFER_REJECTED', 'OFFER_REJECTED'),
    ('CANDIDATE_REJECTED', 'CANDIDATE_REJECTED')
)


class JobPosting(AuditStamp):
    creator = models.UUIDField(editable=False)
    title = models.CharField(max_length=100)
    type = models.CharField(choices=JOB_TYPE, max_length=50)
    category = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    description = models.TextField()
    skills = models.ManyToManyField(Skill)
    min_experience = models.IntegerField()
    max_experience = models.IntegerField()
    vacancies = models.IntegerField()
    status = models.CharField(choices=JOB_POSTING_STATUS, max_length=30)
    company = models.CharField(max_length=200)


class JobApplication(AuditStamp):
    applicant = models.ForeignKey(Profile, on_delete=models.CASCADE)
    jobPosting = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    status = models.CharField(choices=JOB_APPLICATION_STATUS, max_length=30, default='APPLIED')
