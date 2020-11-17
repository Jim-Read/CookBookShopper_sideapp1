from models.Recipe import Recipe
from models.User import User
from main import db
from schemas.RecipeSchema import recipe_schema, recipes_schema
from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.auth_service import verify_user
from sqlalchemy.orm import joinedload

recipes = Blueprint('recipes', __name__, url_prefix="/recipes")

@recipes.route("/", methods=["GET"])
def recipe_index():
    #Retrieve all recipes
    recipes = Recipe.query.options(joinedload("user")).all()
    return jsonify(recipes_schema.dump(recipes))

@recipes.route("/", methods=["POST"])
@jwt_required
@verify_user
def recipe_create(user=None):
    #Create a new recipe
    recipe_fields = recipe_schema.load(request.json)

    new_recipe = Recipe()
    new_recipe.recipe_name = recipe_fields["recipe_name"]
    new_recipe.description = recipe_fields["description"]

    user.recipes.append(new_recipe)

    db.session.commit()
    
    return jsonify(recipe_schema.dump(new_recipe))

@recipes.route("/<int:id>", methods=["GET"])
def recipe_show(id):
    #Return a single recipe
    recipe = Recipe.query.get(id)
    return jsonify(recipe_schema.dump(recipe))

@recipes.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required
@verify_user
def recipe_update(id, user=None):
    #Update a recipe
    recipe_fields = recipe_schema.load(request.json)

    recipes = Recipe.query.filter_by(recipe_id=id, user_id=user.user_id)

    if recipes.count() != 1:
        return abort(401,  description="Unauthorized to update this recipe")    
    
    recipes.update(recipe_fields)
    db.session.commit()

    return jsonify(recipe_schema.dump(recipes[0]))

@recipes.route("/<int:id>", methods=["DELETE"])
@jwt_required
@verify_user
def recipe_delete(id, user=None):
    #Delete a recipe

    recipe = Recipe.query.filter_by(recipe_id=id, user_id=user.user_id).first()

    if not recipe:
        return abort(400)
    
    db.session.delete(recipe)
    db.session.commit()

    return jsonify(recipe_schema.dump(recipe))