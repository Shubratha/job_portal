from django.shortcuts import get_object_or_404
from rest_framework import generics
from .serializers import ProjectSerializer, ProfileSerializer
from rest_framework.response import Response
from .models import Project, Profile
from job_posting.models import JobApplication, JobPosting
from job_posting.serializers import JobApplicationSerializer
from .permissions import IsJobSeekerOrRecruiter
from cs_utils.authentication import JWTAuthentication


class ProfileList(generics.ListCreateAPIView):
    serializer_class = ProfileSerializer
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsJobSeekerOrRecruiter, )

    def get_queryset(self):
        user_id = self.request.user.id
        Profile.objects.filter(creator=user_id)

    def create(self, request, *args, **kwargs):
        user_id = request.user.id
        try:
            Profile.objects.get(creator=user_id)
        except Profile.DoesNotExist:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=201, headers=headers)
        return Response("Already exist", status=400)

    def perform_create(self, serializer):
        user_id = self.request.user.id
        serializer.save(creator=user_id, last_modifier=user_id)


class ProfileDetail(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsJobSeekerOrRecruiter, )

    def get_object(self):
        get_object_or_404(Profile, creator=self.request.user.id)
        return get_object_or_404(Profile, pk=self.kwargs['pk'])

    def patch(self, request, *args, **kwargs):
        profile_id = kwargs['pk']
        current_profile_id = Profile.objects.get(creator=request.user.id).id
        if str(current_profile_id) == profile_id:
            return self.partial_update(request, *args, **kwargs)
        else:
            return Response("Unauthorised User", status=400)


class ProjectList(generics.ListCreateAPIView):
    permission_classes = (IsJobSeekerOrRecruiter, )
    serializer_class = ProjectSerializer
    authentication_classes = (JWTAuthentication, )

    def get_queryset(self):
        profile_id = self.kwargs['profile_id']
        return Project.objects.filter(profile=profile_id)

    def perform_create(self, serializer):
        profile_id = self.kwargs['profile_id']
        current_profile_id = Profile.objects.get(
            creator=self.request.user.id).id
        if str(current_profile_id) == profile_id:
            profile = Profile.objects.get(id=self.kwargs['profile_id'])
            serializer.save(profile=profile)
            return Response("Project created", status=201)
        else:
            return Response("Unauthorised User", status=400)


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsJobSeekerOrRecruiter, )

    def get_object(self):
        profile_id = self.kwargs['profile_id']
        get_object_or_404(Profile, pk=profile_id)
        project_id = self.kwargs['project_id']
        project = get_object_or_404(Project, pk=project_id)
        return project

    def patch(self, request, *args, **kwargs):
        profile_id = self.kwargs['profile_id']
        current_profile_id = Profile.objects.get(
            creator=self.request.user.id).id
        if str(current_profile_id) == profile_id:
            return self.partial_update(request, *args, **kwargs)
        else:
            return Response("Unauthorised User", status=400)


class JobApplicationList(generics.ListCreateAPIView):
    serializer_class = JobApplicationSerializer
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsJobSeekerOrRecruiter, )

    def perform_create(self, serializer):
        profile_id = self.kwargs['profile_id']
        current_profile_id = Profile.objects.get(
            creator=self.request.user.id).id
        if str(current_profile_id) == profile_id:
            profile = Profile.objects.get(id=self.kwargs['profile_id'])
            jobPost = JobPosting.objects.get(id=self.request.data['jobPosting'])
            serializer.save(applicant=profile, jobPosting=jobPost)
            return Response("Application added", status=201)
        else:
            return Response("Unauthorised User", status=400)

    def get_queryset(self):
        profile_id = self.kwargs['profile_id']
        return JobApplication.objects.filter(applicant=profile_id)


class JobApplicationDetail(generics.RetrieveDestroyAPIView):
    serializer_class = JobApplicationSerializer
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsJobSeekerOrRecruiter, )

    def get_object(self):
        profile_id = self.kwargs['profile_id']
        get_object_or_404(Profile, pk=profile_id)
        application_id = self.kwargs['application_id']
        application = get_object_or_404(JobApplication, id=application_id)
        return application
