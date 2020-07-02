from django.test import TestCase
from django.urls import reverse, resolve

class HomePageTest(TestCase):
	def test_home_page_status(self):
		response = resolve('/home/')
		self.assertEquals(response.status_code, 200)