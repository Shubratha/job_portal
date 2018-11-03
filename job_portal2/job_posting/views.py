from django.shortcuts import get_object_or_404
from rest_framework import generics
from .serializers import JobApplicationSerializer
from rest_framework import pagination
# from rest_framework import status
from rest_framework.response import Response
from .models import JobApplication

class JobApplicationList(generics.ListCreateAPIView):
    serializer_class = JobApplicationSerializer

    def perform_create(self, serializer):
        profile = Profile.objects.get(id=self.kwargs['profile_id'])
        serializer.save(profile=profile)
        return Response("Project created", status=201)

    def get_queryset(self):
        profile_id = self.kwargs['profile_id']
        return Project.objects.filter(profile=profile_id)
