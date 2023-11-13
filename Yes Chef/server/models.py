# models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    instructions = db.Column(db.Text)

    # One-to-Many relationship with Ingredient
    ingredients = db.relationship('Ingredient', backref='recipe', lazy=True)

    # Many-to-Many relationship with Tag
    tags = db.relationship('Tag', secondary='recipe_tags', lazy='subquery',
                           backref=db.backref('recipes', lazy=True))

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

# Association table for Many-to-Many relationship between Recipe and Tag
recipe_tags = db.Table('recipe_tags',
                       db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True),
                       db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True))
