from django.test import TestCase
from rest_framework.test import APIClient
from .models import Profile, Project
from job_posting.models import JobApplication, JobPosting
from core.tests import login


class ProfileProject(TestCase):

    def get_api_client(self, role):
        cred = login(role)
        access_token = cred['access_token']
        refresh_token = cred['refresh_token']
        return APIClient(
            HTTP_X_ACCESS_TOKEN=access_token,
            HTTP_X_REFRESH_TOKEN=refresh_token
        )

    def test_valid_test_cases(self):
        client = self.get_api_client('job-seeker')
        profile_info = {
            "first_name": "harry",
            "last_name": "potter",
            "user_type": "Seeker",
            "description": "Im a jobseeker"
        }
        response = client.post("/api/user_profiles/", profile_info)
        response_json = response.data
        profile_uuid = response_json['id']
        url = "/api/user_profiles/" + str(profile_uuid) + "/projects/"
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        content = {
                        'profile': str(profile_uuid),
                        'title': 'New-project',
                        'start_date': '1996-03-03',
                        'end_date': '1996-04-04',
                        'description': 'my first project',
                        'team_size': 1,
                        'role': 'developer',
                        'project_links': 'https://bitbucket.org/codekraftk2/job_portal/src/master/job_portal/'
        }
        response = client.post(url, content)
        self.assertEqual(response.status_code, 201)
        response_json = response.data
        projectID = Project.objects.get(id=response.data['id'])
        url = "/api/user_profiles/" + str(profile_uuid) + "/projects/" + str(projectID.id)
        content = {
                    'id': self.id,
                    'profile': str(profile_uuid),
                    'title': 'New-project',
                    'start_date': '1996-03-03',
                    'end_date': '1996-04-04',
                    'description': 'my first project',
                    'team_size': 1,
                    'role': 'developer/designer',
                    'project_links': 'https://bitbucket.org/codekraftk2/job_portal/src/master/job_portal/'
        }
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        content = {
                    'description': 'updated description'
        }
        response = client.patch(url, content)
        self.assertEqual(response.status_code, 200)
        response = client.delete(url)
        self.assertEqual(response.status_code, 204)


class JobApplicationTest(TestCase):
    def setUp(self):
        self.profile = Profile.objects.create(first_name='harry',
                                              last_name='potter')
        self.jobPosting = JobPosting.objects.create(
            creator="ab35f2483d56421f9ade787b72f6e8af",
            title="Developer",
            type="FULL_TIME",
            location="Bangalore",
            description="Looking for developer with python skills",
            min_experience=0,
            max_experience=5,
            vacancies=2,
            status="POSTED",
            company="Example")

    def get_api_client(self, role):
        cred = login(role)
        access_token = cred['access_token']
        refresh_token = cred['refresh_token']
        return APIClient(
            HTTP_X_ACCESS_TOKEN=access_token,
            HTTP_X_REFRESH_TOKEN=refresh_token
        )

    def test_valid_cases(self):
        client = self.get_api_client('job-seeker')
        profile_info = {
            "first_name": "harry",
            "last_name": "potter",
            "user_type": "Seeker",
            "description": "Im a jobseeker"
        }
        response = client.post("/api/user_profiles/", profile_info)
        response_json = response.json()
        profile_uuid = response_json['id']
        url = "/api/user_profiles/" + str(profile_uuid) + "/applications/"
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        jobPosting_uuid = self.jobPosting.id
        content = {
            "applicant": profile_uuid,
            "jobPosting": jobPosting_uuid,
        }
        response = client.post(url, content)
        self.assertEqual(response.status_code, 201)
        response_json = response.data
        appID = JobApplication.objects.get(id=response_json['id'])
        url = "/api/user_profiles/" + str(profile_uuid) + "/applications/" + str(appID.id)
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        response = client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_invalid_cases(self):
        client = APIClient()
        profile_info = {
            "first_name": "harry",
            "last_name": "potter",
            "user_type": "Seeker",
            "description": "Im a jobseeker"
        }
        response = client.post("/api/user_profiles/", profile_info)
        self.assertEqual(response.status_code, 403)
        client = self.get_api_client('job-seeker')
        response = client.post("/api/user_profiles/", profile_info)
        response_json = response.json()
        profile_uuid = response_json['id']
        url = "/api/user_profiles/" + str(profile_uuid) + "/application/"
        response = client.get(url)
        self.assertEqual(response.status_code, 404)
        invalid_proid = "3621fe5357734dcdaf95a7f329a13cb7"
        url = "/api/user_profiles/" + str(invalid_proid) + "/application/"
        self.assertEqual(response.status_code, 404)
        response = client.post(url, {})
        self.assertEqual(response.status_code, 404)
        invalid_appID = "3040093a86244e9fa9425a35abd29b6c"
        url = "/api/user_profiles/" + str(profile_uuid) + "/applications/" + invalid_appID
        self.assertEqual(response.status_code, 404)
        url = "/api/user_profiles/" + str(profile_uuid) + "/applications/"
        jobPosting_uuid = self.jobPosting.id
        content = {
            "applicant": profile_uuid,
            "jobPosting": jobPosting_uuid,
        }
        response = client.post(url, content)
        response_json = response.data
        url = "/api/user_profiles/" + str(profile_uuid) + "/applications/" + str(response_json['id'])
        response = client.post(url, content)
        self.assertEqual(response.status_code, 405)
        response = client.patch(url, content)
        self.assertEqual(response.status_code, 405)
