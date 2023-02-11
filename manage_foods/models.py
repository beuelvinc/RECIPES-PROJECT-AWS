from django.db import models


class Food(models.Model):
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to='food_images/',blank=True, null=True)
    origin_continent = models.CharField(max_length=50,blank=True, null=True)
    origin_country = models.CharField(max_length=50,blank=True, null=True)
    main_ingredients = models.ManyToManyField("Ingredient")
    recipe = models.TextField(blank=True, null=True)   #Recipe
    youtube_link = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
