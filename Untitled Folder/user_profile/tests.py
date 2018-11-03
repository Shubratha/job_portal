from django.test import TestCase
from rest_framework.test import APIClient
from .models import Profile, Project
from core.models import Address
from core.tests import login
from job_posting.models import JobApplication, JobPosting


class ProfileAddressTest(TestCase):
    def setUp(self):
        self.address = Address.objects.create(address_type="temporary",
                                              city="mysore",
                                              state="Karnatake",
                                              country="India",
                                              postal_code=573229)

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
            "first_name": "abc",
            "last_name": "xyz",
            "user_type": "Seeker",
            "description": "pqr"}
        response = client.post(
            "/api/user_profiles/", profile_info, format='json')
        self.assertEqual(response.status_code, 201)
        profile = Profile.objects.last()
        profile_uuid = profile.id
        url = "/api/user_profiles/" + str(profile_uuid) + "/addresses/"
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        url = "/api/user_profiles/" + str(profile_uuid) + "/addresses/"
        address_uuid = self.address.id
        profileaddress_info = {
            "address": str(address_uuid)
        }
        response = client.post(url, profileaddress_info)
        self.assertEqual(response.status_code, 201)
        url = "/api/user_profiles/" + str(
            profile_uuid) + "/addresses/" + str(address_uuid) + "/"
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        response = client.patch(url, {"line1": "BTM"})

    def test_invalid_cases(self):
        client = self.get_api_client('job-seeker')
        profile_info = {
            "first_name": "abc",
            "last_name": "xyz",
            "user_type": "Seeker",
            "description": "pqr"}
        response = client.post(
            "/api/user_profiles/", profile_info, format='json')
        profile_uuid = response.data['id']
        invalid_proid = "3621fe5357734dcdaf95a7f329a13cb7"
        url = "/api/user_profiles/" + invalid_proid + "/addresses/"
        response = client.get(url)
        self.assertEqual(response.status_code, 404)
        url = "/api/user_profiles/" + str(profile_uuid) + "/addresses/"
        response = client.post(url, {})
        self.assertEqual(response.status_code, 400)
        invalid_addrID = "3040093a86244e9fa9425a35abd29b6c"
        url = "/api/user_profiles/" + str(
            profile_uuid) + "/addresses/" + invalid_addrID + "/"
        response = client.get(url)
        self.assertEqual(response.status_code, 404)
        response = client.delete(url)
        self.assertEqual(response.status_code, 404)

        url = "/api/user_profiles/" + profile_uuid + "/addresses/"
        address_uuid = self.address.id
        url = "/api/user_profiles/" + str(
            profile_uuid) + "/addresses/" + str(address_uuid) + "/"
        response = client.post(url, {})
        self.assertEqual(response.status_code, 405)
        response = client.patch(url, {"postal_code": ""})
        self.assertEqual(response.status_code, 400)


class ProfileAPITest(TestCase):

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
            "first_name": "abc",
            "last_name": "xyz",
            "user_type": "Seeker",
            "description": "pqr"
        }
        response = client.post(
            "/api/user_profiles/", profile_info, format='json')
        self.assertEqual(response.status_code, 201)
        profile_uuid = response.data['id']
        response = client.get(
            "/api/user_profiles/")
        self.assertEqual(response.status_code, 200)
        response = client.post(
            "/api/user_profiles/", profile_info, format='json')
        self.assertEqual(response.status_code, 400)
        url = "/api/user_profiles/" + str(profile_uuid) + "/"
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        response = client.patch(url, {"first_name": "pqr"})
        self.assertEqual(response.status_code, 200)
        response = client.delete(url)
        self.assertEqual(response.status_code, 405)
        client = self.get_api_client('recruiter')
        profile_info_rec = {
            "first_name": "abc",
            "last_name": "xyz",
            "user_type": "Recruiter",
            "description": "pqr"
        }
        response = client.post(
            "/api/user_profiles/", profile_info_rec, format='json')
        self.assertEqual(response.status_code, 201)
        profile_uuid = response.data['id']
        response = client.get(
            "/api/user_profiles/")
        self.assertEqual(response.status_code, 200)
        response = client.post(
            "/api/user_profiles/", profile_info_rec, format='json')
        self.assertEqual(response.status_code, 400)
        url = "/api/user_profiles/" + str(profile_uuid) + "/"
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        response = client.patch(url, {"first_name": "pqr"})
        self.assertEqual(response.status_code, 200)
        response = client.delete(url)
        self.assertEqual(response.status_code, 405)

    def test_invalid_cases(self):
        client = self.get_api_client('job-seeker')
        profile_info = {
            "first_name": "abc",
            "last_name": "xyz",
            "description": "pqr",
            "user_type": "Seeker"}
        response = client.post(
            "/api/user_profile", profile_info, format='json')
        self.assertEqual(response.status_code, 404)
        response = client.get(
            "/api/user_profile", profile_info, format='json')
        self.assertEqual(response.status_code, 404)
        response = client.patch(
            "/api/user_profiles/", {'first': 'pqr'}, format='json')
        self.assertEqual(response.status_code, 405)
        response = client.patch(
            "/api/user_profile", {'first_name': 'pqr'}, format='json')
        self.assertEqual(response.status_code, 404)


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
            'title': 'New-project',
            'start_date': '1996-03-03',
            'end_date': '1996-04-04',
            'description': 'my first project',
            'team_size': 1,
            'role': 'developer',
            'project_links': 'https://bitbucket.org'
        }
        response = client.post(url, content)
        self.assertEqual(response.status_code, 201)
        response_json = response.data
        projectID = Project.objects.get(id=response.data['id'])
        url = "/api/user_profiles/" + str(
            profile_uuid) + "/projects/" + str(projectID.id) + "/"
        content = {
            'id': self.id,
            'title': 'New-project',
            'start_date': '1996-03-03',
            'end_date': '1996-04-04',
            'description': 'my first project',
            'team_size': 1,
            'role': 'developer/designer',
            'project_links': 'https://bitbucket.org'
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

    def test_invalid_test_cases(self):
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
        response = client.put(url, {})
        self.assertEqual(response.status_code, 405)
        client = self.get_api_client('recruiter')
        profile_info_rec = {
            "first_name": "abc",
            "last_name": "xyz",
            "user_type": "Recruiter",
            "description": "pqr"
        }
        response = client.post(
            "/api/user_profiles/", profile_info_rec, format='json')
        url = "/api/user_profiles/" + str(profile_uuid) + "/projects/"
        content = {
            'title': 'New-project',
            'start_date': '1996-03-03',
            'end_date': '1996-04-04',
            'description': 'my first project',
            'team_size': 1,
            'role': 'developer',
            'project_links': 'https://bitbucket.org'
        }
        response = client.post(url, content)
        self.assertEqual(response.status_code, 400)


class EducationAPITest(TestCase):
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
        education_info = {
            "education_type": "regular",
            "course": "MCA",
            "specialization": "CSE",
            "board": "NITC",
            "year_of_passing": "2018-08-20",
            "organization_name": "NITC",
            "score_type": "CGPA",
            "score": "8.00",
            "qualification": "PG"
        }
        profile_info = {
            "first_name": "abc",
            "last_name": "xyz",
            "user_type": "Seeker",
            "description": "pqr"
        }
        response = client.post(
            "/api/user_profiles/", profile_info, format='json')
        self.assertEqual(response.status_code, 201)
        profile_uuid = response.data['id']
        url = "/api/user_profiles/" + str(profile_uuid) + "/educations/"
        response = client.post(url, education_info, format='json')
        self.assertEqual(response.status_code, 201)
        education_uuid = response.data['id']
        url = "/api/user_profiles/" + str(
            profile_uuid) + "/educations/" + str(education_uuid) + "/"
        response = client.patch(url, {"course": "pqr"}, format='json')
        self.assertEqual(response.status_code, 200)
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        response = client.delete(url)
        self.assertEqual(response.status_code, 204)

        client = self.get_api_client('recruiter')
        education_info_rec = {
            "education_type": "regular",
            "course": "MCA",
            "specialization": "CSE",
            "board": "NITC",
            "year_of_passing": "2018-08-20",
            "organization_name": "NITC",
            "score_type": "CGPA",
            "score": "8.00",
            "qualification": "PG"
        }
        profile_info_rec = {
            "first_name": "abc",
            "last_name": "xyz",
            "user_type": "Recruiter",
            "description": "pqr"
        }
        response = client.post(
            "/api/user_profiles/", profile_info_rec, format='json')
        self.assertEqual(response.status_code, 201)
        profile_uuid = response.data['id']
        url = "/api/user_profiles/" + str(profile_uuid) + "/educations/"
        response = client.post(url, education_info_rec, format='json')
        self.assertEqual(response.status_code, 201)
        education_uuid = response.data['id']
        url = "/api/user_profiles/" + str(
            profile_uuid) + "/educations/" + str(education_uuid) + "/"
        response = client.patch(url, {"course": "pqr"}, format='json')
        self.assertEqual(response.status_code, 200)
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        response = client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_invalid_cases(self):
        client = self.get_api_client('job-seeker')
        profile_info = {
            "first_name": "abc",
            "last_name": "xyz",
            "user_type": "Seeker",
            "description": "pqr"
        }
        education_info = {
            "education_type": "regular",
            "course": "MCA",
            "specialization": "CSE",
            "board": "NITC",
            "year_of_passing": "2018-08-20",
            "organization_name": "NITC",
            "score_type": "CGPA",
            "score": "8.00"
        }
        response = client.post(
            "/api/user_profiles/", profile_info, format='json')
        self.assertEqual(response.status_code, 201)
        profile_uuid = response.data['id']
        education_uuid = "c5ad3472-c0e3-43bb-bb62-38b35f13f903"
        response = client.post(
            "/api/user_profiles/" + str(
                profile_uuid) + "/educations/", education_info, format='json')
        self.assertEqual(response.status_code, 400)
        response = client.post(
            "/api/user_profile/" + str(
                profile_uuid) + "/education/", education_info, format='json')
        self.assertEqual(response.status_code, 404)
        url = "/api/user_profiles/" + str(
            profile_uuid) + "/education" + str(education_uuid) + "/"
        response = client.patch(url, {'course': 'pqr'}, format='json')
        self.assertEqual(response.status_code, 404)
        response = client.patch(
            "/api/user_profile", {'course': 'pqr'}, format='json')
        self.assertEqual(response.status_code, 404)


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
        url = "/api/user_profiles/" + str(
            profile_uuid) + "/applications/" + str(appID.id) + "/"
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        client = self.get_api_client('recruiter')
        profile_info_rec = {
            "first_name": "abc",
            "last_name": "xyz",
            "user_type": "Recruiter",
            "description": "pqr"
        }
        response = client.post(
            "/api/user_profiles/", profile_info_rec, format='json')
        recruiterID = response.data['id']
        url = "/api/user_profiles/" + str(
            recruiterID) + "/applications/" + str(appID.id) + "/"
        response = client.patch(url, {"status":'SHORTLISTED'})
        self.assertEqual(response.status_code, 200)
        url = "/api/user_profiles/" + str(
            profile_uuid) + "/applications/" + str(appID.id) + "/"
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
        url = "/api/user_profiles/" + invalid_proid + "/addresses/"
        response = client.get(url)
        self.assertEqual(response.status_code, 404)
        url = "/api/user_profiles/" + str(profile_uuid) + "/addresses/"
        response = client.post(url, {})
        self.assertEqual(response.status_code, 400)
        invalid_addrID = "3040093a86244e9fa9425a35abd29b6c"
        url = "/api/user_profiles/" + str(
            profile_uuid) + "/addresses/" + invalid_addrID + "/"
        response = client.get(url)
        self.assertEqual(response.status_code, 404)
        invalid_appID = "3040093a86244e9fa9425a35abd29b6c"
        url = "/api/user_profiles/" + str(
            profile_uuid) + "/applications/" + invalid_appID
        self.assertEqual(response.status_code, 404)
        url = "/api/user_profiles/" + str(profile_uuid) + "/applications/"
        jobPosting_uuid = self.jobPosting.id
        content = {
            "applicant": profile_uuid,
            "jobPosting": jobPosting_uuid,
        }
        response = client.post(url, content)
        response_json = response.data
        url = "/api/user_profiles/" + str(
            profile_uuid) + "/applications/" + str(response_json['id']) + "/"
        response = client.post(url, content)
        self.assertEqual(response.status_code, 405)
        response = client.patch(url, content)
        self.assertEqual(response.status_code, 405)


class WorkExperienceAPITest(TestCase):

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
        workexperiance_info = {
            "company_name": "codehall",
            "start_date": "2018-01-20",
            "end_date": "2018-08-20",
            "role": "software Developer",
            "description": "abc"
        }
        profile_info = {
            "first_name": "abc",
            "last_name": "xyz",
            "user_type": "Seeker",
            "description": "pqr"
        }
        response = client.post(
            "/api/user_profiles/", profile_info, format='json')
        self.assertEqual(response.status_code, 201)
        profile_uuid = response.data['id']
        url = "/api/user_profiles/" + profile_uuid + "/workexperiences/"
        response = client.post(url, workexperiance_info, format='json')
        self.assertEqual(response.status_code, 201)
        workexperiance_uuid = response.data['id']
        url = "/api/user_profiles/" + str(
            profile_uuid) + "/workexperiences/" + str(
            workexperiance_uuid) + "/"
        response = client.patch(url, {"company_name": "pqr"}, format='json')
        self.assertEqual(response.status_code, 200)
        response = client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_invalid_cases(self):
        client = self.get_api_client('job-seeker')
        profile_uuid = "c5ad3472-c0e3-43bb-bb62-38b35f13f903"
        workexperiance_info = {
            "company_name": "codehall",
            "start_date": "2018-01-20",
            "end_date": "2018-08-20",
            "role": "software Developer",
            "description": "abc"
        }
        response = client.post(
            "/api/user_profile/" + str(
                profile_uuid) + "/workexperience",
            workexperiance_info, format='json')
        self.assertEqual(response.status_code, 404)
        workexperiance_uuid = "c5ad3472-c0e3-43bb-bb62-38b35f13f903"
        url = "/api/user_profiles/" + str(
            profile_uuid) + "/workexperience" + str(workexperiance_uuid) + "/"
        response = client.patch(url, {'company_name': 'pqr'}, format='json')
        self.assertEqual(response.status_code, 404)
        response = client.patch(
            "/api/user_profile", {'company_name': 'pqr'}, format='json')
        self.assertEqual(response.status_code, 404)
        response = client.delete(url)
        self.assertEqual(response.status_code, 404)


class LinkAPITest(TestCase):

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
        link_info = {
            "name": "git",
            "url": "https://github.com/sarvesh"
        }
        profile_info = {
            "first_name": "abc",
            "last_name": "xyz",
            "user_type": "Seeker",
            "description": "pqr"
        }
        response = client.post(
            "/api/user_profiles/", profile_info, format='json')
        self.assertEqual(response.status_code, 201)
        profile_uuid = response.data['id']
        url = "/api/user_profiles/" + str(profile_uuid) + "/links/"
        response = client.post(url, link_info, format='json')
        self.assertEqual(response.status_code, 201)
        link_uuid = response.data['id']
        url = "/api/user_profiles/" + str(
            profile_uuid) + "/links/" + str(link_uuid) + "/"
        response = client.patch(url, {"name": "abc"}, format='json')
        self.assertEqual(response.status_code, 200)
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        response = client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_invalid_cases(self):
        client = self.get_api_client('job-seeker')
        profile_uuid = "c5ad3472-c0e3-43bb-bb62-38b35f13f903"
        link_info = {
            "name": "git",
            "url": "https://github.com/Singhsarvesh"
        }
        response = client.post(
            "/api/user_profile/" + str(
                profile_uuid) + "/links",
            link_info, format='json')
        self.assertEqual(response.status_code, 404)
        link_uuid = "c5ad3472-c0e3-43bb-bb62-38b35f13f903"
        url = "/api/user_profiles/" + str(
            profile_uuid) + "/link/" + str(link_uuid) + "/"
        response = client.patch(url, {"name": "abc"}, format='json')
        self.assertEqual(response.status_code, 404)
        response = client.delete(url)
        self.assertEqual(response.status_code, 404)
