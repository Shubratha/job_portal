from django.urls import re_path, path
from . import views

urlpatterns = [
    path('', views.ProfileList.as_view()),
    re_path(r'^(?P<profile_id>[0-9a-f-]+)/projects/$',
            views.ProjectList.as_view()),
    re_path(r'^(?P<profile_id>[0-9a-f-]+)/projects/(?P<project_id>[0-9a-f-]+)$',
            views.ProjectDetail.as_view()),
    re_path(r'^(?P<profile_id>[0-9a-f-]+)/applications/$',
            views.JobApplicationList.as_view()),
    re_path(r'^(?P<profile_id>[0-9a-f-]+)/applications/(?P<application_id>[0-9a-f-]+)$',
            views.JobApplicationDetail.as_view()),
]

