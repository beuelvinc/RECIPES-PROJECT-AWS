from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Food, Ingredient
from .serializers import FoodSerializer, IngredientSerializer
from django.http import Http404


class FoodList(APIView):
    """
    The `FoodList` class is an APIView that provides a list of Food objects in a RESTful API.
    """

    def get(self, request):
        """
        Retrieve a list of Food objects.

        :param request: The request object that contains the GET parameters.
        :return: A Response object with the serialized Food objects.
        """
        name = request.GET.get('name')
        if name:
            foods = Food.objects.filter(name__iexact=name)
        else:
            foods = Food.objects.all()
        serializer = FoodSerializer(foods, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new Food object.

        :param request: The request object that contains the data for the new Food object.
        :return: A Response object with the serialized data of the created Food object.
        """
        if not request.user.is_superuser:
            return Response({"message": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = FoodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FoodDetail(APIView):
    """
    This class provides the ability to retrieve, update, and delete food items by their name or primary key.
    Only superusers are allowed to perform update and delete actions.
    """

    def get_object(self, pk):
        """
        This helper method retrieves a food item by its primary key (pk).
        If the food item does not exist, a 404 error is raised.

        :param pk: the primary key of the food item
        :return: the food item with the given primary key
        """
        try:
            return Food.objects.get(pk=pk)
        except Food.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        """
        This method retrieves a food item by its name or primary key.
        If neither a name nor a pk is provided, a 400 error is returned.

        :param request: the HTTP request
        :param pk: the primary key of the food item (optional)
        :return: a serialized representation of the food item
        """
        if pk is not None:
            food = self.get_object(pk)
        else:
            return Response({"message": "Please provide either a name or a pk for the food."},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = FoodSerializer(food)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        This method updates a food item by its primary key.
        Only superusers are allowed to perform this action.
        If the food item does not exist, a 404 error is raised.
        If the update is successful, the updated food item is returned.
        If the update fails, a 400 error is returned.

        :param request: the HTTP request
        :param pk: the primary key of the food item
        :return: a serialized representation of the updated food item
        """
        if not request.user.is_superuser:
            return Response({"message": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)
        food = self.get_object(pk)
        serializer = FoodSerializer(food, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        This method deletes a food item by its primary key.
        Only superusers are allowed to perform this action.
        If the delete is successful, a 204 status code is returned.
        If an error occurs while deleting the item, a 500 error is returned.

        :param request: the HTTP request
        :param pk: the primary key of the food item
        :return: a message indicating
        """
        if not request.user.is_superuser:
            return Response({"message": "You do not have permission to perform this action."},
                            status=status.HTTP_401_UNAUTHORIZED)
        try:
            item = self.get_object()
            item.delete()
            return Response({"message": "The item was successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            return Response({"message": "An error occurred while deleting the item."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class IngredientList(APIView):
    """
    API endpoint for managing ingredients.

    Supports GET and POST requests. GET requests can filter ingredients based
    on name or primary key, and returns a list of ingredients in JSON format.
    POST requests are only allowed for superusers, and create a new ingredient.
    """

    def get(self, request):
        """
        Handle GET requests and return a list of ingredients.

        Filters can be applied by passing 'name' or 'pk' as query parameters.
        :param request: the HTTP request
        :return: a message indicating
        """
        name = request.GET.get('name')

        if name:
            Ingredients = Ingredient.objects.filter(name__iexact=name)
        else:
            Ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(Ingredients, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Handle POST requests and create a new ingredient.

        Only superusers are allowed to perform this action.
        :param request: the HTTP request
        :return: a message
        """
        if not request.user.is_superuser:
            return Response({"message": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = IngredientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IngredientDetail(APIView):
    """
    Retrieve, update or delete a ingredient instance.
    """

    def get_object(self, pk):
        """
        Get the ingredient object based on primary key
        :param pk: primary key of the ingredient
        :return: ingredient instance
        :raises: Http404 if the ingredient does not exist
        """
        try:
            return Ingredient.objects.get(pk=pk)
        except Ingredient.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        """
        Get the ingredient details based on name or pk.
        :param request: HttpRequest
        :param pk: primary key of the ingredient
        :return: ingredient instance serialized
        :raises: Http400 if either name or pk is not provided
        """
        if pk is not None:
            ingredient = self.get_object(pk)
        else:
            return Response({"message": "Please provide either a name or a pk for the Ingredient."},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = IngredientSerializer(ingredient)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update the ingredient instance.
        :param request: HttpRequest
        :param pk: primary key of the ingredient
        :return: updated ingredient instance serialized
        :raises: Http403 if user does not have permission
        :raises: Http400 if serialization is not valid
        """
        if not request.user.is_superuser:
            return Response({"message": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)
        ingredient = self.get_object(pk)
        serializer = IngredientSerializer(ingredient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete the ingredient instance.
        :param request: HttpRequest
        :param pk: primary key of the ingredient
        :return: Http204 if the ingredient is deleted successfully
        :raises: Http401 if user does not have permission
        :raises: Http500 if error occurred while deleting the ingredient
        """
        if not request.user.is_superuser:
            return Response({"message": "You do not have permission to perform this action."},
                            status=status.HTTP_401_UNAUTHORIZED)
        try:
            item = self.get_object()
            item.delete()
            return Response({"message": "The item was successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            return Response({"message": "An error occurred while deleting the item."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
