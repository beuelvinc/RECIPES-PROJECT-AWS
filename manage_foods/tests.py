# from django.test import Client, TestCase
# from django.contrib.auth.models import User
# from rest_framework import status
# from .models import Food
# from .serializers import FoodSerializer
#
#
# class TestCaseFoodApi(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(username='testuser', password='password')
#         self.food = Food.objects.create(name='Food 1', recipe="FOOOD")
#         self.valid_payload = {
#             'name': 'Food 2',
#         }
#         self.invalid_payload = {
#             'name': '',
#         }
#
#     def test_get_all_foods(self):
#         response = self.client.get('/api/foods/list')
#         foods = Food.objects.all()
#         serializer = FoodSerializer(foods, many=True)
#         self.assertEqual(response.data, serializer.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_get_valid_single_food(self):
#         response = self.client.get(f'/api/foods/list?name={self.food.name}')
#         food = Food.objects.get(name=self.food.name)
#         serializer = FoodSerializer(food)
#         self.assertEqual(response.data, [serializer.data])
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_get_invalid_single_food(self):
#         response = self.client.get('/api/foods/list?name=invalid')
#         self.assertEqual(response.data, [])
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_create_valid_food(self):
#         self.client.login(username='testuser', password='password')
#         response = self.client.post('/api/foods/list', data=self.valid_payload, content_type='application/json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#     def test_create_invalid_food(self):
#         self.client.login(username='testuser', password='password')
#         response = self.client.post('/api/foods/list/', data=self.invalid_payload, content_type='application/json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_create_food_without_permission(self):
#         response = self.client.post('/api/foods/list/', data=self.valid_payload, content_type='application/json')
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
