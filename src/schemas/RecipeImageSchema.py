from main import ma
from models.RecipeImage import RecipeImage
from marshmallow.validate import Length

class RecipeImageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RecipeImage
    
    filename = ma.String(required=True, validate=Length(min=1))

recipe_image_schema = RecipeImageSchema()