# import unittest
# from django.test import RequestFactory, TestCase
# from .views import get_all_group_players

# class TestGetAllGroupPlayersView(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.invalid_group_id = "invalid_group_id"

#     def test_get_all_group_players_invalid_group_id(self):
#         request = self.factory.get('/get_all_group_players/?group_id=' + self.invalid_group_id)
#         response = get_all_group_players(request)
#         self.assertEqual(response.status_code, 404)