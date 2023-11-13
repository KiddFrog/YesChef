# app.py

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Recipe, Ingredient, Tag, recipe_tags

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db.init_app(app)

# Define routes and application logic here

@app.route("/", methods=['GET'])
def welcome():
    body = "<html><body><h1>Welcome to the test page</h1></body></html>"
    return body

@app.route('/recipes', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.all()
    serialized_recipes = [{'title': recipe.title, 'description': recipe.description, 'instructions': recipe.instructions} for recipe in recipes]
    return jsonify(serialized_recipes)

@app.route('/create_recipe', methods=['POST'])
def create_recipe():
    data = request.get_json()

    # Extract data from the request
    title = data.get('title')
    description = data.get('description')
    instructions = data.get('instructions')
    ingredients = data.get('ingredients', [])  # Assuming ingredients is a list of strings
    tags = data.get('tags', [])  # Assuming tags is a list of strings

    # Create a new recipe
    new_recipe = Recipe(title=title, description=description, instructions=instructions)

    # Add ingredients to the recipe
    for ingredient_name in ingredients:
        ingredient = Ingredient(name=ingredient_name)
        new_recipe.ingredients.append(ingredient)

    # Add tags to the recipe
    for tag_name in tags:
        tag, _ = Tag.query.get_or_create(name=tag_name)
        new_recipe.tags.append(tag)

    # Commit changes to the database
    db.session.add(new_recipe)
    db.session.commit()

    return jsonify({'message': 'Recipe created successfully'})

if __name__ == '__main__':
    app.run(debug=True)
