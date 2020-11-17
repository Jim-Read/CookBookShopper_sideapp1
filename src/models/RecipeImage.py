from main import db

class RecipeImage(db.Model):
    __tablename__ = "recipe_images"

    image_id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String())
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.recipe_id"), nullable=False)

    def __repr__(self):
        return f"<BookImage {self.filename}>"