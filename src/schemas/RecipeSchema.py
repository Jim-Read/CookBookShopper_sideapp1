from main import ma
from models.Recipe import Recipe
from marshmallow.validate import Length
from schemas.UserSchema import UserSchema

class RecipeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Recipe

    recipe_name = ma.String(required=True, validate=Length(max=40))
    description = ma.String(required=True, validate=Length(max=40))
    recipe_image = ma.String(required=False, validate=Length(min=1))
    user = ma.Nested(UserSchema)
    
recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True)