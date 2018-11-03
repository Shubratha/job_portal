from django.db import models
from core.models import AuditStamp, Address
from user_profile.models import Profile


COMPANY_STATUS = (
    ('ACTIVE', 'ACTIVE'),
    ('INACTIVE', 'INACTIVE')
)
COMPANY_TYPE = (
    ('PRIVATE', 'PRIVATE'),
    ('PUBLIC', 'PUBLIC')
)


ADDRESS_TYPE = (
    ('PERMANENT', 'PERMANENT'),
    ('TEMPORARY', 'TEMPORARY')
)


class Company(AuditStamp):
    name = models.CharField(max_length=200)
    description = models.TextField()
    website = models.URLField()
    size = models.IntegerField()
    type = models.TextField(choices=COMPANY_TYPE)
    status = models.TextField(choices=COMPANY_STATUS, default='ACTIVE')

    def __str__(self):  # pragma: no cover
        return self.name


class CompanyAddress(AuditStamp):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE,
                                related_name='companyaddress')

    def __str__(self):  # pragma: no cover
        return '{} - {}'.format(self.company, self.address)


class CompanyRecruiter(AuditStamp):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    recruiter = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("company", "recruiter")

    def __str__(self):  # pragma: no cover
        return '{} - {}'.format(self.company, self.recruiter)
