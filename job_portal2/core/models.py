import uuid
from django.db import models


ADDRESS_TYPE = (
    ('PERMANENT', 'PERMANENT'),
    ('TEMPORARY', 'TEMPORARY')
)


class AuditStamp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    creator = models.UUIDField(
        default=uuid.uuid4
    )
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modifier = models.UUIDField(
        default=uuid.uuid4
    )
    last_modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Skill(AuditStamp):
    name = models.CharField(max_length=100, unique=True)


class Address(AuditStamp):
    address_type = models.CharField(max_length=200)
    line1 = models.CharField(max_length=300)
    line2 = models.CharField(max_length=300)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    postal_code = models.IntegerField()
