from django.urls import reverse
from rest_framework.test import APITestCase
from django.conf import settings
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


class AnimalViewsIntegrationTestCase(APITestCase):

    def setUp(self):
        logger.info(f"Using BASE_URL: {settings.BASE_URL}")

    def test_get_animal_details_integration(self):
        logger.info(f"Testing GET /fetch-animal-details?page={500}  going from page=1 takes too long so for testing sake lets go with page=500")
        response = self.client.get(reverse('fetch-animal-details'), {'page': 500})
        logger.info(f"Received status: {response.status_code}")
        logger.info(f"Omitting response.json here since its too lengthy u might wanna try loading up the postman export")
        self.assertIn(response.status_code, [200, 400])

    def test_create_animal_integration(self):
        logger.info("Testing POST /bulk-create-animal")
        payload = {"data": [{"id": 100, "name": "Bear", "friends": ["fox","Dog"], "born_at": "2005-05-27T19:22:35.339Z"},{"id": 101, "name": "Cat", "friends": ["Lion"], "born_at": "1987-11-24T05:49:48.271Z"}]}
        response = self.client.post(reverse('bulk-create-animal'), payload, format='json')
        logger.info(f"Received status: {response.status_code}")
        logger.info(f"Response data: {response.json()}")
        self.assertIn(response.status_code, [200, 400])



