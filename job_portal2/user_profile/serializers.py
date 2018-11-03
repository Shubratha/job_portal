from rest_framework import serializers
from .models import Project, Profile


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = (
            'id', 'first_name',
            'last_name','description','user_type', 'skills')
        depth = 2


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('id', 'title', 'start_date',
                          'end_date', 'description',
                          'team_size', 'role', 'project_links')

