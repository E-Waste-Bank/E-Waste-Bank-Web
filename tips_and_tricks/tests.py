from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import *
from .forms import *

# Create your tests here.

class TipsViewsTest(TestCase):
    def setUp(self):
        self.admin_group = Group(name="admin")
        self.admin_group.save()

        self.user = get_user_model().objects.create_user(username="t3st_us3r", password='us3r_t3st', email='test@user.xyz')
        self.user.save()

        self.user_b = get_user_model().objects.create_user(username="t3st_us3rb", password='us3r_t3stb', email='testb@user.xyz')
        self.user_b.save()

        self.user_admin = get_user_model().objects.create_user(username="admt3st_us3rb", password='admus3r_t3stb', email='admtestb@user.xyz')
        self.user_admin.groups.add(self.admin_group)
        self.user_admin.save()

        self.client = Client()
        self.client.login(username="t3st_us3r", password='us3r_t3st')

        self.client_b = Client()
        self.client_b.login(username="t3st_us3rb", password='us3r_t3stb')

        self.client_admin = Client()
        self.client_admin.login(username="admt3st_us3rb", password='admus3r_t3stb')

    def tearDown(self):
        self.client.logout()
        self.user.delete()      

    def test_tips_page_200(self):
        response = self.client.get("/tips-and-tricks/")
        self.assertEqual(response.status_code, 200) 

    def test_tips_add_page_200(self):
        response = self.client_admin.get("/tips-and-tricks/add")
        self.assertEqual(response.status_code, 200) 