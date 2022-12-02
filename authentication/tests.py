from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

# Create your tests here.
class AuthenticationViewsTest(TestCase):
    def setUp(self):
        self.admin_group = Group(name="admin")
        self.admin_group.save()

        self.user = get_user_model().objects.create_user(username="t3st_us3r", password='us3r_t3st', email='test@user.xyz')
        self.user.save()

        self.user_b_inac = get_user_model().objects.create_user(username="t3st_us3rb", password='us3r_t3stb', email='testb@user.xyz')
        self.user_b_inac.is_active = False
        self.user_b_inac.save()

        self.user_admin = get_user_model().objects.create_user(username="admt3st_us3rb", password='admus3r_t3stb', email='admtestb@user.xyz')
        self.user_admin.groups.add(self.admin_group)
        self.user_admin.save()

    def test_login_user_success(self):
        client = Client()
        response = client.post('/auth/login/', {'username': 't3st_us3r', 'password': 'us3r_t3st'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['role'], 'user')

    def test_login_admin_success(self):
        client = Client()
        response = client.post('/auth/login/', {'username': 'admt3st_us3rb', 'password': 'admus3r_t3stb'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['role'], 'admin')

    def test_login_inactive(self):
        client = Client()
        response = client.post('/auth/login/', {'username': 't3st_us3rb', 'password': 'us3r_t3stb'})
        self.assertEqual(response.status_code, 401)

    def test_login_user_wrong_username(self):
        client = Client()
        response = client.post('/auth/login/', {'username': 'iamnotavalidusern4me', 'password': 'us3r_t3st'})
        self.assertEqual(response.status_code, 401)

    def test_login_user_wrong_password(self):
        client = Client()
        response = client.post('/auth/login/', {'username': 'admt3st_us3rb', 'password': 'iamnotavalidpassw0rd'})
        self.assertEqual(response.status_code, 401)
