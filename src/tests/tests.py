import unittest
from main import create_app, db
from models.Recipe import Recipe

class TestRecipes(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()
        db.create_all()

        runner = cls.app.test_cli_runner()
        runner.invoke(args=["db", "seed"])

    @classmethod
    def tearDown(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()
    
    def test_recipe_index(self):
        response = self.client.get("/recipes/")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)

    def test_recipe_create(self):
        response = self.client.post("/recipes/", json={
            "recipe_name": "Test Recipe",
            "description": "A very good Recipe",
            "recipe_image": "http://"
        })

        data = response.get_json()

        #self.assertEqual(response.status_code, 200)
        self.assertTrue(bool(response.status_code >= 200 and response.status_code < 300))
        self.assertIsInstance(data, dict)
        self.assertTrue(bool("recipe_id" in data.keys()))

        recipe = Recipe.query.get(data["recipe_id"])
        self.assertIsNotNone(recipe)

    def test_pizza_delete(self):
        recipe = Recipe.query.first()

        response = self.client.delete(f"/recipes/{recipe.recipe_id}")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)

        recipe = Recipe.query.get(recipe.recipe_id)
        self.assertIsNone(recipe)