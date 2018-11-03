from rest_framework import serializers
from company.models import Company
from .models import CompanyRecruiter
from user_profile.models import Profile
from company.models import CompanyAddress


class CompanySerializer(serializers.ModelSerializer):
        class Meta:
            model = Company
            fields = '__all__'


class RecruiterSerializer(serializers.ModelSerializer):
        class Meta:
            model = Profile
            fields = '__all__'


class CompanyRecruiterSerializer(serializers.ModelSerializer):

        company = CompanySerializer(read_only=True)
        recruiter = RecruiterSerializer(read_only=True)

        class Meta:
            model = CompanyRecruiter
            fields = ('id', 'company', 'recruiter')


class CompanyAddressSerializer(serializers.ModelSerializer):

        class Meta:
            model = CompanyAddress
            fields = ('address', )
            depth = 2
