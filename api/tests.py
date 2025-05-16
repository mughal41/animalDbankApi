from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch


class AnimalViewsTestCase(APITestCase):

    @patch("api.views.fetch_all_animal_details_with_threads")
    def test_get_animal_details_success(self, mock_fetch):
        mock_fetch.return_value = [{"id": 1, "name": "Tiger", "friends": ["Lion"], "born_at": 1672531200000}]
        response = self.client.get(reverse('fetch-animal-details'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("status"), "success")


    @patch("api.views.fetch_all_animal_details_with_threads")
    def test_get_animal_details_failure(self, mock_fetch):
        mock_fetch.return_value = None
        response = self.client.get(reverse('fetch-animal-details'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get("status"), "failed")

    @patch("api.views.bulk_parse_data")
    def test_create_animal_success(self, mock_bulk):
        mock_bulk.return_value = True
        payload = {"data": [{"id": 1, "name": "Tiger", "friends": "Lion", "born_at": 1672531200000}]}
        response = self.client.post(reverse('bulk-create-animal'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("status"), "success")

    @patch("api.views.bulk_parse_data")
    def test_create_animal_failure(self, mock_bulk):
        mock_bulk.return_value = False
        payload = {"data": [{"name": "Elephant", "friends": "", "born_at": None}]}
        response = self.client.post(reverse('bulk-create-animal'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get("status"), "failed")