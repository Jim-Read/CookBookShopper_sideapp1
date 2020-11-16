from main import db

class Recipe(db.Model):
    __tablename__ = "recipes"

    recipe_id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String())
    description = db.Column(db.String())
    recipe_image = db.Column(db.String())