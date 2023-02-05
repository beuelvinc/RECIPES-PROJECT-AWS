from rest_framework.views import APIView
from rest_framework.response import Response
from .open_ai import Request as OpenAIRequest
from youtubesearchpython import VideosSearch
from .models import Food
import logging
import traceback

logger = logging.getLogger('django')


class ListFoods(APIView):
    """
    The class handles User request to send a request to 3rd libraries
    """

    def get(self, request, *args, **kwargs):
        """
        the function takes post request and proceeds for OPENAI
        :param request: request data
        :return:  Response of status
        """

        try:
            if self.request.data.get("ingredients"):

                ingredients = self.request.data.get("ingredients")
                ingredients = " ,".join(ingredients)
                openai_req = OpenAIRequest()
                open_res = openai_req.get_list_food(ingredients).replace("\n", "")
                filtered = ''.join(filter(lambda c: not c.isdigit(), open_res))
                list_of_foods = filtered.split(".")
                list_of_foods = [i for i in list_of_foods if i]

                return Response({
                    "Ready Response": list_of_foods
                })
            else:
                return Response({
                    "message": "error, send ingredients with same key",
                })
        except BaseException as e:
            err = traceback.format_exception()
            logger.error(err)


class DetailFood(APIView):
    """
    The class handles User request to send a request to 3rd libraries
    """

    def insert_to_table(self, food_name):
        """
        :param food_name: str, contains food name
        :return: nothing
        """
        try:
            if not Food.objects.get(name__iexact=food_name):
                Food.objects.create(name=food_name)

        except BaseException as e:
            err = traceback.format_exception()
            logger.error(err)

    def get(self, request, *args, **kwargs):
        """
        the function takes post request and proceeds for OPENAI and Youtube API
        :param request: request data
        :return:  Response of status
        """
        try:
            if self.request.data.get("name") and self.request.data.get("ingredients"):
                food_name = self.request.data.get("name")

                ingredients = self.request.data.get("ingredients")
                openai_req = OpenAIRequest()

                ready_response = []
                response_youtube = VideosSearch(food_name, limit=1).result().get("result")[0].get("link")
                recipe = openai_req.get_recipe(food_name, ingredients)
                ready_response.append({"Name": food_name, "link": response_youtube, "recipe": recipe})

                return Response({
                    "Ready Response": ready_response
                })
            else:
                return Response({
                    "message": "error, send ingredients with same key",
                })
        except BaseException as e:
            err = traceback.format_exception()
            logger.error(err)
