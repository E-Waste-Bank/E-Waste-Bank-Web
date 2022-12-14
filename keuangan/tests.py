from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import *
from .forms import *

# Create your tests here.

class KeuanganUserViewsTest(TestCase):
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

        self.unauthenticated_client = Client()

        self.client = Client()
        self.client.login(username="t3st_us3r", password='us3r_t3st')

        self.client_b = Client()
        self.client_b.login(username="t3st_us3rb", password='us3r_t3stb')

        self.client_admin = Client()
        self.client_admin.login(username="admt3st_us3rb", password='admus3r_t3stb')

        self.keuangan_data = KeuanganAdmin.objects.create(user=self.user, uang_user=1003074.24)
        self.keuangan_data_b = KeuanganAdmin.objects.create(user=self.user_b, uang_user=0.20)

    def tearDown(self):
        self.client.logout()
        self.user.delete()

    def test_keuangan_page_routing_admin(self):
        response = self.client_admin.get("/keuangan/")
        self.assertRedirects(response, "/keuangan/admin/")

    def test_keuangan_page_routing_user(self):
        response = self.client.get("/keuangan/")
        self.assertRedirects(response, "/keuangan/user/")

    def test_keuangan_user_page_html_response_ok(self):
        response = self.client.get("/keuangan/user/")
        self.assertEqual(response.status_code, 200)

    def test_keuangan_user_page_html_template(self):
        response = self.client.get("/keuangan/user/")
        self.assertTemplateUsed(response, "user.html")

    def test_keuangan_user_data_json_response_ok(self):
        response = self.client.get("/keuangan/json/user/")
        self.assertEqual(response.status_code, 200)

    def test_keuangan_user_data_json_api_response_403(self):
        response = self.unauthenticated_client.get("/keuangan/json/user-api/")
        self.assertEqual(response.status_code, 403)

    def test_keuangan_user_data_json_api_response_ok(self):
        response = self.client.get("/keuangan/json/user-api/")
        self.assertEqual(response.status_code, 200)

    def test_keuangan_user_get_all_cashout_response_ok(self):
        response = self.client.get("/keuangan/json/user-cashouts/")
        self.assertEqual(response.status_code, 200)

    def test_keuangan_user_get_all_cashouts_json_api_response_403(self):
        response = self.unauthenticated_client.get("/keuangan/json/user-cashouts-api/")
        self.assertEqual(response.status_code, 403)

    def test_keuangan_user_get_all_cashouts_json_api_response_200(self):
        response = self.client.get("/keuangan/json/user-cashouts-api/")
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

    def test_keuangan_user_cashout_as_admin_html_200(self):
        cashout_obj = Cashout.objects.create(user=self.user, uang_model=self.keuangan_data, amount=20000)
        cashout_obj.save()
        
        response = self.client_admin.get(f"/keuangan/cashout/{cashout_obj.pk}/")
        self.assertEqual(response.status_code, 200)


class KeuanganUserFormsTest(TestCase):
    def test_cashout_form_valid_data(self):
        valid_data = {'amount': '100000'}
        form = CreateCashoutForm(data = valid_data)
        self.assertTrue(form.is_valid())
    
    def test_cashout_form_invalid_NaN_data(self):
        invalid_data = {'amount': 'NotANumber'}
        form = CreateCashoutForm(data = invalid_data)
        self.assertFalse(form.is_valid())

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

class KeuanganAdminTest(TestCase):
    def setUp(self):
        self.admin_group = Group(name='admin')
        self.admin_group.save()

        self.admin =  get_user_model().objects.create_user(username="tes1admin", password='tes1admintes1admin', email='tes1admin@user.xyz')
        self.admin.groups.add(self.admin_group)
        self.admin.save()

        self.user =  get_user_model().objects.create_user(username="tes2user", password='tes2usertes2user', email='tes2user@user.xyz')
        self.user.save()

        self.user2 =  get_user_model().objects.create_user(username="tes3user", password='tes3usertes3user', email='tes2user@user.xyz')
        self.user.save()        

        self.client_admin = Client()
        self.client_admin.login(username="tes1admin", password="tes1admintes1admin")
        
        self.client_user = Client()
        self.client_user.login(username="tes2user", password="tes2usertes2user")
        
        self.client_user2 = Client()
        self.client_user2.login(username="tes3user", password="tes3usertes3user")

    def tearDown(self):
        self.client.logout()
        self.user.delete()

    # ----------------------------------------------------
    # Tes autorisasi page admin dan user diakses oleh masing-masing role
    # ----------------------------------------------------
    def test_user_access_keuanganAdmin(self):
        response = self.client_user.get("/keuangan/admin/")
        self.assertRedirects(response, "/keuangan/user/")
    
    def test_user_access_keuangan(self):
        response = self.client_user.get("/keuangan/")
        self.assertRedirects(response, "/keuangan/user/")

    def test_admin_access_keuangan(self):
        response = self.client_admin.get("/keuangan/")
        self.assertRedirects(response, "/keuangan/admin/")
    
    # ----------------------------------------------------
    # Tes view json admin
    # ----------------------------------------------------
    def test_keuangan_admin_get_all_cashout_response_ok(self):
        response = self.client_admin.get("/keuangan/json/admin-cashouts/")
        self.assertEqual(response.status_code, 200)
    
    def test_keuangan_admin_get_all_uang_user_response_ok(self):
        response = self.client_admin.get("/keuangan/json/admin/")
        self.assertEqual(response.status_code, 200)
    
    def test_keuangan_admin_cashout_html_response_false(self):
        response = self.client_admin.get(f"/keuangan/edit-cashout/9999999999/")
        self.assertNotEqual(response.status_code, 200)
    
    def test_keuangan_admin_uang_user_html_response_false(self):
        response = self.client_admin.get(f"/keuangan/edit-uang-user/9999999999/")
        self.assertNotEqual(response.status_code, 200)
    
class KeuanganAdminFormsTest(TestCase):
    def test_uang_user_form_admin_success(self):
        valid_data = {'uang_user': '123.11'}
        form = EditUangUserForm(data = valid_data)
        self.assertTrue(form.is_valid())
    
    def test_uang_user_form_admin_false(self):
        invalid_data = {'uang_user': '#PSDisFun'}
        form = EditUangUserForm(data = invalid_data)
        self.assertFalse(form.is_valid())