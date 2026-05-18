from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Animal


class AnimalPublicReadTests(APITestCase):
    def setUp(self):
        Animal.objects.create(
            raca='Vira-lata',
            data_acolhimento='2026-01-10',
            status='disponivel'
        )
        Animal.objects.create(
            raca='Poodle',
            data_acolhimento='2026-02-10',
            status='acolhido'
        )

    def _extract_results(self, response):
        if isinstance(response.data, dict) and 'results' in response.data:
            return response.data['results']
        return response.data

    def test_list_animals_is_public(self):
        response = self.client.get(reverse('animal-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(self._extract_results(response)), 1)

    def test_disponivel_filter_returns_only_available_animals(self):
        response = self.client.get(reverse('animal-list'), {'disponivel': 'true'})
        data = self._extract_results(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['status'], 'disponivel')

    def test_create_animal_still_requires_authentication(self):
        payload = {
            'raca': 'Labrador',
            'data_acolhimento': '2026-03-15',
            'status': 'disponivel'
        }

        response = self.client.post(reverse('animal-list'), payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
