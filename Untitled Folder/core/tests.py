from django.test import TestCase
import json
import requests


class HelloWorldTest(TestCase):
    def test_hello_world(self):
        response = self.client.get('/hello_world')
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(content['hello'], 'world')


def login(role):
    # import ipdb; ipdb.set_trace()
    credentials_by_role = {
        'company-owner': {
            'email': 'c@company.com',
            'password': 'company_owner@2018'
        },
        'recruiter': {
            'email': 'r@recruiter.com',
            'password': 'recruiter@2018'
        },
        'company-rep': {
            'email': 'rep@rep.com',
            'password': 'rep@2018'
        },
        'job-seeker': {
            'email': 's@seeker.com',
            'password': 'seeker@2018'
        }
    }
    if role not in credentials_by_role:
        raise TypeError("Invalid Role received")
    cred = credentials_by_role[role]
    try:
        response = requests.post('http://localhost:8000/api/login/', data=cred)
    except requests.exceptions.RequestException:
        raise Exception("Unable to Access Auth Service")
    return response.json()
