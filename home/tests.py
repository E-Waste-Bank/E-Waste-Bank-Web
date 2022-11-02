from django.test import TestCase, Client

# Create your tests here.
class LandingPageViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def tearDown(self):
        pass

    # def test_landing_page_html_response_ok(self):
    #     response = self.client.get("/")
    #     self.assertEqual(response.status_code, 200)

    # def test_landing_page_html_template(self):
    #     response = self.client.get("/")
    #     self.assertTemplateUsed(response, "landing_page.html")

    # TODO tests of register POST, login POST, logout (w/ user)
    def test_login_user_page_html_response_ok(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)

    def test_register_user_page_html_response_ok(self):
        response = self.client.get("/register/")
        self.assertEqual(response.status_code, 200)

