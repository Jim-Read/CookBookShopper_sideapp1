from models.Recipe import Recipe
from main import db
from schemas.RecipeSchema import recipe_schema, recipes_schema
from flask import Blueprint, request, jsonify
recipes = Blueprint('recipes', __name__, url_prefix="/recipes")

@recipes.route("/", methods=["GET"])
def recipe_index():
    #Retrieve all recipes
    recipes = Recipe.query.all()
    return jsonify(recipes_schema.dump(recipes))



@recipes.route("/", methods=["POST"])
def recipe_create():
    #Create a new recipe
    recipe_fields = recipe_schema.load(request.json)

    new_recipe = Recipe()
    new_recipe.recipe_name = recipe_fields["recipe_name"]
    new_recipe.description = recipe_fields["description"]
    new_recipe.recipe_image = recipe_fields["recipe_image"]
    
    db.session.add(new_recipe)
    db.session.commit()
    
    return jsonify(recipe_schema.dump(new_recipe))


@recipes.route("/<int:id>", methods=["GET"])
def recipe_show(id):
    #Return a single recipe
    recipe = Recipe.query.get(id)
    return jsonify(recipe_schema.dump(recipe))


@recipes.route("/<int:recipe_id>", methods=["PUT", "PATCH"])
def recipe_update(recipe_id):
    #Update a recipe
    recipes = Recipe.query.filter_by(recipe_id=recipe_id)
    recipe_fields = recipe_schema.load(request.json)
    recipes.update(recipe_fields)
    db.session.commit()

    return jsonify(recipe_schema.dump(recipes[0]))


@recipes.route("/<int:id>", methods=["DELETE"])
def book_delete(id):
    #Delete a recipe
    recipe = Recipe.query.get(id)
    db.session.delete(recipe)
    db.session.commit()

    return jsonify(recipe_schema.dump(recipe))