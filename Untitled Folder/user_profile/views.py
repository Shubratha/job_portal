from django.shortcuts import get_object_or_404
from rest_framework import generics
from core.models import Address
from rest_framework.response import Response
from .models import (ProfileAddress, Profile, Project,
                     Education, WorkExperience, Link)
from cs_utils.authentication import JWTAuthentication
from .permissions import (IsJobSeekerOrRecruiter,
                          IsJobSeeker, IsRecruiter)
from .serializers import (
    ProfileSerializer, EducationSerializer,
    ProfileAddressSerializer, AddressSerializer,
    ProjectSerializer,
    WorkExperienceSerializer, LinkSerializer)
from job_posting.models import JobApplication, JobPosting
from job_posting.serializers import JobApplicationSerializer


class ProfileList(generics.ListCreateAPIView):
    serializer_class = ProfileSerializer
    authentication_classes = (JWTAuthentication, )
    permission_classes = ((IsJobSeeker or IsRecruiter),)
    permission_classes = (IsJobSeekerOrRecruiter, )

    def get_queryset(self):
        user_id = self.request.user.id
        return Profile.objects.filter(creator=user_id)

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
    permission_classes = ((IsJobSeeker or IsRecruiter),)
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


class EducationList(generics.CreateAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    lookup_url_kwarg = 'pk'
    authentication_classes = (JWTAuthentication, )
    permission_classes = ((IsJobSeeker or IsRecruiter),)
    permission_classes = ((IsJobSeeker or IsRecruiter),)

    def perform_create(self, serializer):
        profile_id = self.kwargs['pk']
        current_profile_id = Profile.objects.get(
            creator=self.request.user.id).id
        if str(current_profile_id) == profile_id:
            profile_id = Profile.objects.get(id=self.kwargs['pk'])
            serializer.save(
                profile=profile_id,
                creator=self.request.user.id,
                last_modifier=self.request.user.id
            )
            return Response("Education created", status=201)
        else:
            return Response("Unauthorised User", status=400)


class EducationDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EducationSerializer
    authentication_classes = (JWTAuthentication, )
    permission_classes = ((IsJobSeeker or IsRecruiter),)

    def get_object(self):
        get_object_or_404(Profile, pk=self.kwargs['pk'])
        education = get_object_or_404(
            Education, pk=self.kwargs['education_id'])
        return education

    def patch(self, request, *args, **kwargs):
        profile_id = kwargs['pk']
        current_profile_id = Profile.objects.get(creator=request.user.id).id
        if str(current_profile_id) == profile_id:
            return self.partial_update(request, *args, **kwargs)
        else:
            return Response("Unauthorised User", status=400)

    def destroy(self, request, *args, **kwargs):
        profile_id = kwargs['pk']
        current_profile_id = Profile.objects.get(creator=request.user.id).id
        if str(current_profile_id) == profile_id:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response("Record deleted", status=204)
        else:
            return Response("Unauthorised User", status=400)


class WorkExperienceList(generics.CreateAPIView):
    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer
    authentication_classes = (JWTAuthentication, )
    permission_classes = ((IsJobSeeker or IsRecruiter),)

    def perform_create(self, serializer):
        profile_id = self.kwargs['pk']
        current_profile_id = Profile.objects.get(
            creator=self.request.user.id).id
        if str(current_profile_id) == profile_id:
            profile_id = Profile.objects.get(id=self.kwargs['pk']).id
            serializer.save(
                profile_id=profile_id,
                creator=self.request.user.id,
                last_modifier=self.request.user.id
            )
            return Response("WorkExperience created", status=201)


class WorkExperienceDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkExperienceSerializer
    authentication_classes = (JWTAuthentication, )
    permission_classes = ((IsJobSeeker or IsRecruiter),)

    def get_object(self):
        get_object_or_404(Profile, pk=self.kwargs['pk'])
        workExperience = get_object_or_404(
            WorkExperience, pk=self.kwargs['wk_id'])
        return workExperience

    def patch(self, request, *args, **kwargs):
        profile_id = self.kwargs['pk']
        current_profile_id = Profile.objects.get(
            creator=self.request.user.id).id
        if str(current_profile_id) == profile_id:
            return self.partial_update(request, *args, **kwargs)
        else:
            return Response("Unauthorised User", status=400)

    def destroy(self, request, *args, **kwargs):
        profile_id = kwargs['pk']
        current_profile_id = Profile.objects.get(creator=request.user.id).id
        if str(current_profile_id) == profile_id:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response("Record deleted", status=204)
        else:
            return Response("Unauthorised User", status=400)


class LinkList(generics.CreateAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    authentication_classes = (JWTAuthentication, )
    permission_classes = ((IsJobSeeker or IsRecruiter),)

    def perform_create(self, serializer):
        profile_id = Profile.objects.get(id=self.kwargs['pk'])
        profile_id = self.kwargs['pk']
        current_profile_id = Profile.objects.get(
            creator=self.request.user.id).id
        if str(current_profile_id) == profile_id:
            serializer.save(
                profile_id=profile_id,
                creator=self.request.user.id,
                last_modifier=self.request.user.id
            )
            return Response("Profile Link created", status=201)
        else:
            return Response("Unauthorised User", status=400)


class LinkDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LinkSerializer
    authentication_classes = (JWTAuthentication, )
    permission_classes = ((IsJobSeeker or IsRecruiter),)

    def get_object(self):
        get_object_or_404(Profile, pk=self.kwargs['pk'])
        link = get_object_or_404(
            Link, pk=self.kwargs['link_id'])
        return link

    def patch(self, request, *args, **kwargs):
        profile_id = self.kwargs['pk']
        current_profile_id = Profile.objects.get(
            creator=self.request.user.id).id
        if str(current_profile_id) == profile_id:
            return self.partial_update(request, *args, **kwargs)
        else:
            return Response("Unauthorised User", status=400)

    def destroy(self, request, *args, **kwargs):
        profile_id = kwargs['pk']
        current_profile_id = Profile.objects.get(creator=request.user.id).id
        if str(current_profile_id) == profile_id:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response("Record deleted", status=204)
        else:
            return Response("Unauthorised User", status=400)


class ProfileAddressList(generics.ListCreateAPIView):
    serializer_class = ProfileAddressSerializer
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsJobSeekerOrRecruiter, )

    def perform_create(self, serializer):
        profile = Profile.objects.get(id=self.kwargs['profile_id'])
        current_profile_id = Profile.objects.get(
            creator=self.request.user.id).id
        if str(current_profile_id) == str(profile.id):
            addressID = self.request.data['address']
            address = Address.objects.get(id=addressID)
            serializer.save(profile=profile, address=address)
        else:
            return Response("Unauthorised access", status=400)

    def get_queryset(self):
        profile = get_object_or_404(Profile, pk=self.kwargs['profile_id'])
        return ProfileAddress.objects.filter(profile=profile)


class ProfileAddressDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsJobSeekerOrRecruiter, )

    def get_object(self):
        profile_id = self.kwargs['profile_id']
        get_object_or_404(Profile, pk=profile_id)
        address_id = self.kwargs['address_id']
        address = get_object_or_404(Address, pk=address_id)
        return address

    def patch(self, request, *args, **kwargs):
        profile = Profile.objects.get(id=self.kwargs['profile_id'])
        current_profile_id = Profile.objects.get(creator=request.user.id).id
        if current_profile_id == profile.id:
            return self.partial_update(request, *args, **kwargs)
        else:
            return Response("Unauthorised access", status=400)

    def destroy(self, request, *args, **kwargs):
        profile_id = kwargs['profile_id']
        current_profile_id = Profile.objects.get(creator=request.user.id).id
        if str(current_profile_id) == profile_id:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response("Record deleted", status=204)
        else:
            return Response("Unauthorised User", status=400)


class ProjectList(generics.ListCreateAPIView):
    permission_classes = (IsJobSeekerOrRecruiter, )
    serializer_class = ProjectSerializer
    authentication_classes = (JWTAuthentication, )

    def get_queryset(self):
        profile_id = self.kwargs['profile_id']
        return Project.objects.filter(profile=profile_id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile_id = self.kwargs['profile_id']
        current_profile_id = Profile.objects.get(
            creator=self.request.user.id).id
        if str(current_profile_id) == profile_id:
            self.perform_create(serializer)
            return Response(serializer.data, status=201)
        else:
            return Response("Unauthorised User", status=400)

    def perform_create(self, serializer):
        profile_id = self.kwargs['profile_id']
        current_profile_id = Profile.objects.get(
            creator=self.request.user.id).id
        if str(current_profile_id) == profile_id:
            profile = Profile.objects.get(id=self.kwargs['profile_id'])
            serializer.save(profile=profile)


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

    def destroy(self, request, *args, **kwargs):
        profile_id = kwargs['profile_id']
        current_profile_id = Profile.objects.get(creator=request.user.id).id
        if str(current_profile_id) == profile_id:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response("Record deleted", status=204)
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
            jobPost = JobPosting.objects.get(
                id=self.request.data['jobPosting'])
            serializer.save(applicant=profile, jobPosting=jobPost)
            return Response("Application added", status=201)
        else:
            return Response("Unauthorised User", status=400)

    def get_queryset(self):
        profile_id = self.kwargs['profile_id']
        return JobApplication.objects.filter(applicant=profile_id)


class JobApplicationDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JobApplicationSerializer
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsJobSeekerOrRecruiter, )

    def get_object(self):
        profile_id = self.kwargs['profile_id']
        get_object_or_404(Profile, pk=profile_id)
        application_id = self.kwargs['application_id']
        application = get_object_or_404(JobApplication, id=application_id)
        return application

    def perform_update(self, serializer):
        jobPosting = serializer.data['jobPosting']
        recruiterID = JobPosting.objects.get(id=jobPosting).creator
        if(recruiterID == self.request.user.id):
            serializer.save()
        else:
            return Response("Unauthorised editing", status=400)
