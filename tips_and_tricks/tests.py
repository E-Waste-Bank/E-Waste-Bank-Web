from django.test import Client, TestCase
from django.contrib.auth import get_user_model

# Create your tests here.
class TipsAndTrickTestCase(TestCase):
    def test_html(self):
        response = self.client.get('/tips-and-tricks/add/')
        return self.assertEqual(response.status_code, 200)

    def setUp(self):
        self.user = get_user_model().objects.create_user(username="t3st_us3r", 
        password='us3r_t3st', email='test@user.xyz')
        self.user.save()
        self.client = Client()
        self.client.login(username="t3st_us3r", password='us3r_t3st')