from django.test import TestCase
from django.urls import reverse


class AccountRoutesTest(TestCase):

	def test_account_index_is_reachable(self):
		response = self.client.get(reverse('account:index'))
		self.assertEqual(response.status_code, 200)

	def test_login_route_is_reachable(self):
		response = self.client.get(reverse('account:login'))
		self.assertEqual(response.status_code, 200)
