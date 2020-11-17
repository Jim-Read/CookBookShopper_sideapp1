from flask import Blueprint, request, jsonify, abort, current_app, Response
from flask_jwt_extended import jwt_required
from services.auth_service import verify_user
from models.RecipeImage import RecipeImage
from models.Recipe import Recipe
from schemas.RecipeImageSchema import recipe_image_schema
import boto3
from main import db
from pathlib import Path

recipe_images = Blueprint("recipe_images",  __name__, url_prefix="/recipes/<int:recipe_id>/images")

@recipe_images.route("/", methods=["POST"])
@jwt_required
@verify_user
def recipe_image_create(recipe_id, user=None):
    recipe = Recipe.query.filter_by(recipe_id=recipe_id, user_id=user.user_id).first()

    if not recipe:
        return abort(401, description="Invalid recipe")
    
    if "image" not in request.files:
        return  abort(400, description="No Image")
    
    image = request.files["image"]

    if Path(image.filename).suffix not in [".png", ".jpeg", ".jpg", ".gif"]:
        return abort(400, description="Invalid file type")

    filename = f"{recipe_id}{Path(image.filename).suffix}"
    bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
    key = f"recipe_images/{filename}"

    bucket.upload_fileobj(image, key)

    if not recipe.recipe_image:
        new_image = RecipeImage()
        new_image.filename = filename
        recipe.recipe_image = new_image
        db.session.commit()
    
    return ("", 201)

@recipe_images.route("/<int:id>", methods=["GET"])
def recipe_image_show(recipe_id, id):
    recipe_image = RecipeImage.query.filter_by(recipe_id=id).first()

    if not recipe_image:
        return abort(401, description="Invalid recipe")

    bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
    filename = recipe_image.filename
    file_obj = bucket.Object(f"recipe_images/{filename}").get()

    print(file_obj)

    return Response(
        file_obj["Body"].read(),
        mimetype="image/*",
        headers={"Content-Disposition": "attachment;filename=image"}
    )

@recipe_images.route("/<int:id>", methods=["DELETE"])
@jwt_required
@verify_user
def recipe_image_delete(recipe_id, id, user=None):
    recipe = Recipe.query.filter_by(recipe_id=id, user_id=user.user_id).first()

    if not recipe:
        return abort(401, description="Invalid recipe")
    
    if recipe.recipe_image:
        bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
        filename = recipe.recipe_image.filename

        bucket.Object(f"recipe_images/{filename}").delete()

        db.session.delete(recipe.recipe_image)
        db.session.commit()

    return ("", 204)