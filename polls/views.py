from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import urllib.request
import urllib.parse
import json 

def get_Recipes(search):
    search = search.replace(" ","%20")
    
    url = "https://api.edamam.com/api/recipes/v2?type=public&q=" + search + "&app_id=6bef399e&app_key=cc4d4b804b9ddc917ba1f15ea28babc4"
    recipe_name,recipe_ingredients, recipe_id,recipe_image,count = _create_list(get_json_file(url))

    data = {"list" :[], "Search size":count}
    i = 0   
    while i < count:
        data["list"].append({"recipe" : recipe_name[i], "ingredients": recipe_ingredients[i], "image":recipe_image, "recipe_id":recipe_id[i]})
        i+=1
    return data 
"""
Given a url to the search, return the json_file
"""
def get_json_file(url):
    try:
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        json_text = response.read().decode(encoding = 'utf-8')
        json_data = json.loads(json_text)
        return json_data
    finally:
        if(response != None):
            response.close()

"""
Given a json_file return the recipe name, ingredients, id and image
"""
def _create_list(json_file):
    recipe_name = []
    recipe_ingredients = []
    recipe_id = []
    recipe_image = []

    count = 0
    for index in range(len(json_file["hits"])):
        recipe = json_file["hits"][index]
        
        if count > 20:
            return [recipe_name,recipe_ingredients,recipe_id,recipe_image,count]
        recipe_name.append(recipe["recipe"]["label"])
        recipe_image.append(recipe["recipe"]["image"])
        recipe_ingredients.append(recipe["recipe"]["ingredientLines"])
        start = recipe["recipe"]["uri"].find("_")
        recipe_id.append(recipe["recipe"]["uri"][start:])
        count+=1

    return [recipe_name,recipe_ingredients,recipe_id,recipe_image,count]
def index(request):
    return JsonResponse( get_Recipes("lamb"))  
