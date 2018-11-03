from rest_framework import serializers
from .models import (ProfileAddress, Profile,
                     Education, Project, WorkExperience, Link)
from core.models import Address


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = (
            'id', 'first_name',
            'last_name', 'user_type', 'description', 'skills')
        depth = 2


class ProfileAddressSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ProfileAddress
        fields = ('id', 'profile', 'address')
        # depth=2


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'


class EducationSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Education
        fields = ('__all__')


class WorkExperienceSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = WorkExperience
        fields = ('__all__')


class LinkSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Link
        fields = ('__all__')


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = (
            'id',
            'title', 'start_date',
            'end_date', 'description',
            'team_size', 'role', 'project_links')
