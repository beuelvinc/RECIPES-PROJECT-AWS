import os
import openai


class Request:

    def __send(self, prompt):
        """
        :param prompt: sentence
        :return: response from openai
        """
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.6,
            max_tokens=150,
            top_p=1,
            frequency_penalty=1,
            presence_penalty=1
        )
        return response.get("choices")[0].get("text")

    def get_list_food(self, prompt):
        """

        :param prompt: sentence
        :return:
        """
        prompt = "What kind of foods I can make based on the only these ingredients : {} .Give maximum 5 foods".format(
            prompt)
        return self.__send(prompt)

    def get_recipe(self, food, ingredients):
        """
        :param prompt: str sentence
        :param ingredients: str  ingretients
        :return:
        """
        prompt = "List steps of {} to make using only and only :{}".format(food, ingredients)
        return self.__send(prompt)
