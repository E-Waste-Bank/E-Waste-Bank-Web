from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import *

# Create your tests here.

class KeuanganUserViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="t3st_us3r", password='us3r_t3st', email='test@user.xyz')
        self.user.save()

        self.user_b = get_user_model().objects.create_user(username="t3st_us3rb", password='us3r_t3stb', email='testb@user.xyz')
        self.user_b.save()

        self.client = Client()
        self.client.login(username="t3st_us3r", password='us3r_t3st')

        self.client_b = Client()
        self.client_b.login(username="t3st_us3rb", password='us3r_t3stb')

        self.keuangan_data = KeuanganAdmin.objects.create(user=self.user, uang_user=1003074.24)
        self.keuangan_data_b = KeuanganAdmin.objects.create(user=self.user_b, uang_user=0.20)

    def tearDown(self):
        self.client.logout()
        self.user.delete()

    def test_keuangan_user_page_html_response_ok(self):
        response = self.client.get("/keuangan/user/")
        self.assertEqual(response.status_code, 200)

    def test_keuangan_user_page_html_template(self):
        response = self.client.get("/keuangan/user/")
        self.assertTemplateUsed(response, "user.html")

    def test_keuangan_user_data_json_response_ok(self):
        response = self.client.get("/keuangan/json/user/")
        self.assertEqual(response.status_code, 200)

    def test_keuangan_user_get_all_cashout_response_ok(self):
        response = self.client.get("/keuangan/json/user-cashouts/")
        self.assertEqual(response.status_code, 200)

    def test_keuangan_user_create_cashout_response_405(self):
        response = self.client.get("/keuangan/user/create-cashout/")
        self.assertEqual(response.status_code, 405)

    def test_keuangan_user_create_cashout_response_400_negative(self):
        response = self.client.post("/keuangan/user/create-cashout/", {'amount': '-10000'})
        self.assertEqual(response.status_code, 400)

    def test_keuangan_user_create_cashout_response_400_invalid(self):
        response = self.client.post("/keuangan/user/create-cashout/", {'amount': 'a'})
        self.assertEqual(response.status_code, 400)

    def test_keuangan_user_create_cashout_response_400_funds(self):
        response = self.client_b.post("/keuangan/user/create-cashout/", {'amount': '10000'})
        self.assertEqual(response.status_code, 400)

    def test_keuangan_user_create_cashout_response_200(self):
        response = self.client.post("/keuangan/user/create-cashout/", {'amount': '10000'})
        self.assertEqual(response.status_code, 200)

    def test_keuangan_user_cashout_html_response_403_200(self):
        cashout_obj = Cashout.objects.create(user=self.user, uang_model=self.keuangan_data, amount=10000)
        cashout_obj.save()

        response_200 = self.client.get(f"/keuangan/cashout/{cashout_obj.pk}/")
        self.assertEqual(response_200.status_code, 200)

        # ga boleh diakses sm user lain hrsnya
        response_403 = self.client_b.get(f"/keuangan/cashout/{cashout_obj.pk}/")
        self.assertEqual(response_403.status_code, 403)

    def test_keuangan_user_cashout_html_response_404(self):
        response = self.client.get(f"/keuangan/cashout/118181818181/")
        self.assertEqual(response.status_code, 404)

class CashoutModelsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="t3st_us3r", password='us3r_t3st', email='test@user.xyz')
        self.user.save()

        self.client = Client()
        self.client.login(username="t3st_us3r", password='us3r_t3st')

        self.keuangan_data = KeuanganAdmin.objects.create(user=self.user, uang_user=1003074.24)

    def test_cashout_model_creation(self):
        cashout_model = Cashout(
            user=self.user, 
            uang_model=self.keuangan_data, 
            amount=0.10, 
            approved=False, 
            disbursed=False
        )

    def tearDown(self):
        self.client.logout()
        self.user.delete()