from django.test import TestCase
from .models import Company
from core.models import Address
from rest_framework.test import APIClient
from core.tests import login


class CompanyAPITest(TestCase):

    def get_api_client(self, role):
        cred = login(role)
        access_token = cred['access_token']
        refresh_token = cred['refresh_token']
        return APIClient(
            HTTP_X_ACCESS_TOKEN=access_token,
            HTTP_X_REFRESH_TOKEN=refresh_token
        )

    def test_create_company(self):
        client = self.get_api_client('company-owner')
        company_info = {
            "name": "codekraft",
            "description": "this is a good company",
            "website": "http://www.codekraft.in",
            "size": 500,
            "type": "PRIVATE"}

        response = client.post("/api/companies/", company_info, format='json')
        self.assertEqual(response.status_code, 201)

        response_json = response.json()

        c = Company.objects.get(id=response_json['id'])
        for key, value in company_info.items():
            self.assertEqual(getattr(c, key), value)

    def test_create_company_error(self):
        """
        website is not a valid URL
        """
        client = self.get_api_client('company-owner')
        company_info = {
            "name": "codekraft",
            "description": "this is a good company",
            "website": "www.codekraft",
            "size": 500,
            "type": "PRIVATE"
        }

        response = client.post("/api/companies/", company_info, format='json')
        self.assertEqual(response.status_code, 400)


class CompanyRecruiterAPITest(TestCase):

    def get_api_client(self, role):
        cred = login(role)
        access_token = cred['access_token']
        refresh_token = cred['refresh_token']
        return APIClient(
            HTTP_X_ACCESS_TOKEN=access_token,
            HTTP_X_REFRESH_TOKEN=refresh_token
        )

    def test_companies_recruiter_post(self):
        client = self.get_api_client('company-owner')
        company_info = {
            "name": "codekraft",
            "description": "this is a good company",
            "website": "http://www.codekraft.in",
            "size": 500,
            "type": "PRIVATE"}

        response = client.post("/api/companies/", company_info, format='json')
        self.assertEqual(response.status_code, 201)
        response_json = response.json()
        company_id = response_json['id']

        client = self.get_api_client('recruiter')
        recruiter_info = {
            "first_name": "debasis",
            "last_name": "das",
            "user_type": "Recruiter",
            "description": "abc"
        }

        response = client.post(
            "/api/user_profiles/", recruiter_info, format='json')
        self.assertEqual(response.status_code, 201)
        response_json = response.json()
        recruiter_id = response_json['id']
        client = self.get_api_client('company-owner')
        recruiter_info = {
            "recruiter": recruiter_id}
        response = client.post(
            "/api/companies/{}/recruiters/".format
            (company_id), recruiter_info, format='json')
        self.assertEqual(response.status_code, 201)

    def test_companies_recruiter_post_error_case(self):
        client = self.get_api_client('company-owner')
        company_info = {
            "name": "codekraft",
            "description": "this is a good company",
            "website": "http://www.codekraft.in",
            "size": 500,
            "type": "PRIVATE"}

        response = client.post("/api/companies/", company_info, format='json')
        self.assertEqual(response.status_code, 201)
        response_json = response.json()
        client = self.get_api_client('recruiter')
        recruiter_info = {
            "first_name": "debasis",
            "last_name": "das",
            "user_type": "Recruiter",
            "description": "abc"
        }
        response = client.post(
            "/api/user_profiles/", recruiter_info, format='json')
        self.assertEqual(response.status_code, 201)
        response_json = response.json()
        recruiter_id = response_json['id']
        client = self.get_api_client('company-owner')
        recruiter_info = {
            "recruiter": recruiter_id}
        response = client.post(
            "/api/companies/{}/recruiters/".format
            (123), recruiter_info, format='json')
        self.assertEqual(response.status_code, 404)

    def test_companies_recruiter_delete(self):
        client = self.get_api_client('company-owner')
        company_info = {
            "name": "codekraft",
            "description": "this is a good company",
            "website": "http://www.codekraft.in",
            "size": 500,
            "type": "PRIVATE"}

        response = client.post("/api/companies/", company_info, format='json')
        self.assertEqual(response.status_code, 201)

        response_json = response.json()
        company_id = response_json['id']

        client = self.get_api_client('recruiter')
        recruiter_info = {
            "first_name": "debasis",
            "last_name": "das",
            "user_type": "Recruiter",
            "description": "abc"
        }

        response = client.post(
            "/api/user_profiles/", recruiter_info, format='json')
        self.assertEqual(response.status_code, 201)
        response_json = response.json()
        recruiter_id = response_json['id']
        client = self.get_api_client('company-owner')
        recruiter_info = {
            "recruiter": recruiter_id}
        response = client.post("/api/companies/{}/recruiters/".format(
            company_id), recruiter_info, format='json')
        self.assertEqual(response.status_code, 201)

        response = client.delete("/api/companies/{}/recruiters/{}/".format(
            company_id, recruiter_id))
        self.assertEqual(response.status_code, 204)

    def test_companies_recruiter_delete_error_case(self):
        client = self.get_api_client('company-owner')
        company_info = {
            "name": "codekraft",
            "description": "this is a good company",
            "website": "http://www.codekraft.in",
            "size": 500,
            "type": "PRIVATE"}

        response = client.post("/api/companies/", company_info, format='json')
        self.assertEqual(response.status_code, 201)

        response_json = response.json()
        company_id = response_json['id']
        recruiter_id = 1234

        response = client.delete("/api/companies/{}/recruiters/{}/".format(
            company_id, recruiter_id))
        self.assertEqual(response.status_code, 404)


class CompanyAddressAPITest(TestCase):

    def get_api_client(self, role):
        cred = login(role)
        access_token = cred['access_token']
        refresh_token = cred['refresh_token']
        return APIClient(
            HTTP_X_ACCESS_TOKEN=access_token,
            HTTP_X_REFRESH_TOKEN=refresh_token)

    def test_companies_addresses_post(self):
        client = self.get_api_client('company-owner')
        company_info = {
            "name": "codekraft",
            "description": "this is a good company",
            "website": "http://www.codekraft.in",
            "size": 500,
            "type": "PRIVATE"}

        response = client.post("/api/companies/", company_info, format='json')
        self.assertEqual(response.status_code, 201)
        response_json = response.json()
        c = Company.objects.get(id=response_json['id'])
        client = self.get_api_client('company-owner')
        company_address_info = {
            "address_type": "PERMANENT",
            "line1": "1/4 2nd street Koramangala",
            "line2": "Madiwala, Bangalore",
            "city": "Bangalore",
            "state": "Karnataka",
            "country": "India",
            "postal_code": 121212}

        response = client.post("/api/companies/{}/addresses/".format(
            response_json['id']), company_address_info, format='json')
        self.assertEqual(response.status_code, 201)

        response_json = response.json()

        c = Address.objects.get(id=response_json['id'])
        for key, value in company_address_info.items():
            self.assertEqual(getattr(c, key), value)

    def test_companies_addresses_post_error_case(self):
        client = self.get_api_client('company-owner')
        company_info = {
            "name": "codekraft",
            "description": "this is a good company",
            "website": "http://www.codekraft.in",
            "size": 500,
            "type": "PRIVATE"}

        response = client.post("/api/companies/", company_info, format='json')
        self.assertEqual(response.status_code, 201)
        response_json = response.json()
        client = self.get_api_client('company-owner')
        company_address_info = {
            "address_type": "PERMANENT",
            "line1": "1/4 2nd street Koramangala",
            "line2": "Madiwala, Bangalore",
            "city": "Bangalore",
            "state": "Karnataka",
            "country": "India"}

        response = client.post("/api/companies/{}/addresses/".format(
            response_json['id']), company_address_info, format='json')
        self.assertEqual(response.status_code, 400)

    def test_companies_addresses_get(self):
        client = self.get_api_client('company-owner')
        company_info = {
            "name": "codekraft",
            "description": "this is a good company",
            "website": "http://www.codekraft.in",
            "size": 500,
            "type": "PRIVATE"}

        response = client.post("/api/companies/", company_info, format='json')
        self.assertEqual(response.status_code, 201)

        response_json = response.json()

        c = Company.objects.get(id=response_json['id'])

        client = self.get_api_client('company-owner')
        company_address_info = {
            "address_type": "PERMANENT",
            "line1": "1/4 2nd street Koramangala",
            "line2": "Madiwala, Bangalore",
            "city": "Bangalore",
            "state": "Karnataka",
            "country": "India",
            "postal_code": 121212}

        response = client.post("/api/companies/{}/addresses/".format(
            response_json['id']), company_address_info, format='json')
        self.assertEqual(response.status_code, 201)
        response = client.get("/api/companies/{}/addresses/".format(
            response_json['id']))
        self.assertEqual(response.status_code, 200)

        c = Address.objects.first()
        for key, value in company_address_info.items():
            self.assertEqual(getattr(c, key), value)

    def test_companies_addresses_get_error_case(self):
        client = self.get_api_client('company-owner')
        company_info = {
            "name": "codekraft",
            "description": "this is a good company",
            "website": "http://www.codekraft.in",
            "size": 500,
            "type": "PRIVATE"}

        response = client.post("/api/companies/", company_info, format='json')
        self.assertEqual(response.status_code, 201)
        response_json = response.json()
        client = self.get_api_client('company-owner')
        company_address_info = {
            "address_type": "PERMANENT",
            "line1": "1/4 2nd street Koramangala",
            "line2": "Madiwala, Bangalore",
            "city": "Bangalore",
            "state": "Karnataka",
            "country": "India",
            "postal_code": 121212}
        response = client.post("/api/companies/{}/addresses/".format(
            response_json['id']), company_address_info, format='json')
        self.assertEqual(response.status_code, 201)
        response = client.get("/api/companies/{}/addresses/".format(1324))
        self.assertEqual(response.status_code, 404)

    def test_companies_address_get(self):
        client = self.get_api_client('company-owner')
        company_info = {
            "name": "codekraft",
            "description": "this is a good company",
            "website": "http://www.codekraft.in",
            "size": 500,
            "type": "PRIVATE"}

        response = client.post("/api/companies/", company_info, format='json')
        self.assertEqual(response.status_code, 201)
        response_json = response.json()
        company_id = response_json['id']
        client = self.get_api_client('company-owner')
        company_address_info = {
            "address_type": "PERMANENT",
            "line1": "1/4 2nd street Koramangala",
            "line2": "Madiwala, Bangalore",
            "city": "Bangalore",
            "state": "Karnataka",
            "country": "India",
            "postal_code": 121212}
        response = client.post("/api/companies/{}/addresses/".format(
            company_id), company_address_info, format='json')
        self.assertEqual(response.status_code, 201)
        response_json = response.json()
        address_id = response_json['id']
        response = client.get("/api/companies/{}/addresses/{}/".format(
            company_id, address_id))
        self.assertEqual(response.status_code, 200)
        c = Address.objects.first()
        for key, value in company_address_info.items():
            self.assertEqual(getattr(c, key), value)

    def test_companies_address_get_error_case(self):

        client = self.get_api_client('company-owner')
        company_info = {
            "name": "codekraft",
            "description": "this is a good company",
            "website": "http://www.codekraft.in",
            "size": 500,
            "type": "PRIVATE"}
        response = client.post("/api/companies/", company_info, format='json')
        self.assertEqual(response.status_code, 201)
        response_json = response.json()
        company_id = response_json['id']
        client = self.get_api_client('company-owner')
        company_address_info = {
            "address_type": "PERMANENT",
            "line1": "1/4 2nd street Koramangala",
            "line2": "Madiwala, Bangalore",
            "city": "Bangalore",
            "state": "Karnataka",
            "country": "India",
            "postal_code": 121212}
        response = client.post("/api/companies/{}/addresses/".format(
            company_id), company_address_info, format='json')
        self.assertEqual(response.status_code, 201)
        response_json = response.json()
        response = client.get("/api/companies/{}/addresses/{}/".format(
            company_id, 123))
        self.assertEqual(response.status_code, 404)

    def test_companies_addresses_delete(self):
        client = self.get_api_client('company-owner')
        company_info = {
            "name": "codekraft",
            "description": "this is a good company",
            "website": "http://www.codekraft.in",
            "size": 500,
            "type": "PRIVATE"}

        response = client.post("/api/companies/", company_info, format='json')
        self.assertEqual(response.status_code, 201)
        response_json = response.json()
        company_id = response_json['id']
        client = self.get_api_client('company-owner')
        company_address_info = {
            "address_type": "PERMANENT",
            "line1": "1/4 2nd street Koramangala",
            "line2": "Madiwala, Bangalore",
            "city": "Bangalore",
            "state": "Karnataka",
            "country": "India",
            "postal_code": 121212}

        response = client.post("/api/companies/{}/addresses/".format(
            company_id), company_address_info, format='json')
        self.assertEqual(response.status_code, 201)
        response_json = response.json()
        address_id = response_json['id']
        response = client.delete("/api/companies/{}/addresses/{}/".format(
            company_id, address_id))
        self.assertEqual(response.status_code, 204)

    def test_companies_addresses_delete_error_case(self):
        client = self.get_api_client('company-owner')
        company_info = {
            "name": "codekraft",
            "description": "this is a good company",
            "website": "http://www.codekraft.in",
            "size": 500,
            "type": "PRIVATE"}
        response = client.post("/api/companies/", company_info, format='json')
        self.assertEqual(response.status_code, 201)
        response_json = response.json()
        company_id = response_json['id']
        client = self.get_api_client('company-owner')
        company_address_info = {
            "address_type": "PERMANENT",
            "line1": "1/4 2nd street Koramangala",
            "line2": "Madiwala, Bangalore",
            "city": "Bangalore",
            "state": "Karnataka",
            "country": "India",
            "postal_code": 121212}

        response = client.post("/api/companies/{}/addresses/".format(
            company_id), company_address_info, format='json')
        self.assertEqual(response.status_code, 201)
        response_json = response.json()
        address_id = response_json['id']
        response = client.delete("/api/companies/{}/addresses/{}/".format(
            company_id, address_id))
        self.assertEqual(response.status_code, 204)
        response = client.get("/api/companies/{}/addresses/{}/".format(
            company_id, address_id))
        self.assertEqual(response.status_code, 404)

    def test_companies_addresses_put(self):
        client = self.get_api_client('company-owner')
        company_info = {
            "name": "codekraft",
            "description": "this is a good company",
            "website": "http://www.codekraft.in",
            "size": 500,
            "type": "PRIVATE"}
        response = client.post("/api/companies/", company_info, format='json')
        self.assertEqual(response.status_code, 201)
        response_json = response.json()
        company_id = response_json['id']
        client = self.get_api_client('company-owner')
        company_address_info = {
            "address_type": "PERMANENT",
            "line1": "1/4 2nd street Koramangala",
            "line2": "Madiwala, Bangalore",
            "city": "Bangalore",
            "state": "Karnataka",
            "country": "India",
            "postal_code": 121212}

        response = client.post("/api/companies/{}/addresses/".format(
            company_id), company_address_info, format='json')
        self.assertEqual(response.status_code, 201)
        response_json = response.json()
        address_id = response_json['id']
        response_json = response.json()
        c = Address.objects.get(id=response_json['id'])
        for key, value in company_address_info.items():
            self.assertEqual(getattr(c, key), value)

        client = self.get_api_client('company-owner')
        company_address_info = {
            "address_type": "PERMANENT",
            "line1": "1/4 2nd street Koramangala",
            "line2": "Madiwala, Bangalore",
            "city": "Bangalore",
            "state": "Karnataka",
            "country": "India",
            "postal_code": 121212}

        response = client.put("/api/companies/{}/addresses/{}/".format(
            company_id, address_id), company_address_info, format='json')
        self.assertEqual(response.status_code, 204)

    def test_companies_addresses_put_error_case(self):
        client = self.get_api_client('company-owner')
        company_info = {
            "name": "codekraft",
            "description": "this is a good company",
            "website": "http://www.codekraft.in",
            "size": 500,
            "type": "PRIVATE"}
        response = client.post("/api/companies/", company_info, format='json')
        self.assertEqual(response.status_code, 201)
        response_json = response.json()
        company_id = response_json['id']
        client = self.get_api_client('company-owner')
        company_address_info = {
            "address_type": "PERMANENT",
            "line1": "1/4 2nd street Koramangala",
            "line2": "Madiwala, Bangalore",
            "city": "Bangalore",
            "state": "Karnataka",
            "country": "India",
            "postal_code": 121212}

        response = client.post("/api/companies/{}/addresses/".format(
            company_id), company_address_info, format='json')
        self.assertEqual(response.status_code, 201)
        response_json = response.json()
        response_json = response.json()
        c = Address.objects.get(id=response_json['id'])
        for key, value in company_address_info.items():
            self.assertEqual(getattr(c, key), value)
        client = self.get_api_client('company-owner')
        company_address_info = {
            "address_type": "PERMANENT",
            "line1": "1/4 2nd street Koramangala",
            "line2": "Madiwala, Bangalore",
            "city": "Bangalore",
            "state": "Karnataka",
            "country": "India",
            "postal_code": 121212}
        response = client.put("/api/companies/{}/addresses/{}/".format(
            122, 123), company_address_info, format='json')
        self.assertEqual(response.status_code, 404)
