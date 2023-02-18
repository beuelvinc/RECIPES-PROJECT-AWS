from django.test import Client, TestCase
from auth_app.models import User
from rest_framework import status
from rest_framework.test import APIClient
from .models import Food, Ingredient
from .serializers import FoodSerializer
from django.urls import reverse


class TestCaseFoodApi(TestCase):
    """
    Test case for Food API
    """

    def setUp(self):
        """
        Setup function for test case
        initializing necessary pre-steps
        """
        self.client = Client()
        self.cred = {
            'email': "testuser@gmail.com",
            'password': "password"
        }

        self.user = User.objects.create_superuser(email=self.cred.get("email"), password=self.cred.get("password"))
        self.food = Food.objects.create(name='Food 1', recipe="FOOOD")
        self.ingredient = Ingredient.objects.create(name='Food 1')
        self.url_token = reverse('token_obtain_pair')  # gets url
        response = self.client.post(self.url_token, self.cred, format='json')
        self.client.login(email=self.cred.get("email"), password=self.cred.get("password"))
        self.token = response.data['access']
        self.client.defaults['Authorization'] = f'Bearer {self.token}'

        self.valid_payload = {
            'name': 'Food 2',
        }
        self.invalid_payload = {
            'name': '',
        }

    def test_get_all_foods(self):
        """
        Test for getting all foods
        """
        response = self.client.get('/api/foods/list')

        foods = Food.objects.all()
        serializer = FoodSerializer(foods, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_food(self):
        """
        Test for getting a valid single food
        """
        response = self.client.get(f'/api/foods/list?name={self.food.name}')
        food = Food.objects.get(name=self.food.name)
        serializer = FoodSerializer(food)
        self.assertEqual(response.data, [serializer.data])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_nonexisting_single_food(self):
        """
        Test for getting non-existing single food
        """
        response = self.client.get('/api/foods/list?name=Noexist')
        self.assertEqual(response.data, [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_valid_food(self):
        """
        Test for creating a valid food
        """
        self.valid_payload['main_ingredients'] = [self.ingredient.id]
        response = self.client.post('/api/foods/list/', data=self.valid_payload, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    def test_create_invalid_food(self):
        """
        Test for creating an invalid food 
        """
        response = self.client.post('/api/foods/list/', data=self.valid_payload, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_invalid_food(self):
        """
        Test for creating an invalid food
        """
        self.valid_payload['main_ingredients'] = [self.ingredient.id]
        response = self.client.post('/api/foods/list/', data=self.invalid_payload, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
