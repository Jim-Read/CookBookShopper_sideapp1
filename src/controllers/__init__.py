from controllers.recipes_controller import recipes
from controllers.auth_controller  import auth
from controllers.recipe_images_controller import recipe_images

registerable_controllers = [
    auth,
    recipes,
    recipe_images
]