from main import db
from models.RecipeImage import RecipeImage

class Recipe(db.Model):
    __tablename__ = "recipes"
    
    recipe_id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String())
    description = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    recipe_image = db.relationship("RecipeImage", backref="recipe", uselist=False)

    def __repr__(self):
        return f"<recipe {self.recipe_name}>"