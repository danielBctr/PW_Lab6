from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from database.db import db
from database.Recipe import Recipe
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

routes = Blueprint('routes', __name__)

@routes.route('/token', methods=['POST'])
def token():
    try:
        data = request.get_json()
        roles = data.get('roles', [])
        access_token = create_access_token(identity={'roles': roles})
        return jsonify(access_token=access_token), 200
    except:
        return {"message": "Failed to generate token"}, 500

@routes.route('/recipes', methods=['POST'])
@jwt_required(optional=True)  # JWT token is optional for adding recipes
def add_recipe():
    try:
        data = request.get_json()
        recipe = Recipe(
            id=data['id'], title=data['title'], ingredients=data['ingredients'],
            instructions=data['instructions'], servings=data['servings'],
            prep_time=data.get('prep_time'), cook_time=data.get('cook_time'),
            cuisine=data.get('cuisine'), difficulty=data.get('difficulty')
        )
        db.session.add(recipe)
        db.session.commit()
        return {"message": "Recipe added"}, 201
    except IntegrityError:
        db.session.rollback()
        return {"message": "Recipe could not be added. It may already exist or the data provided is not valid."}, 400

@routes.route('/recipes', methods=['GET'])
def get_recipes():
    limit = request.args.get('limit', default=10, type=int)
    offset = request.args.get('offset', default=0, type=int)

    if limit < 0 or offset < 0:
        return {"message": "Invalid values for limit or offset. They must be non-negative."}, 400

    total_recipes = Recipe.query.count()
    if offset >= total_recipes:
        return {"message": "Offset is too large. There are not that many recipes."}, 400

    recipes = Recipe.query.offset(offset).limit(limit).all()
    return jsonify({recipe.id: recipe.to_dict() for recipe in recipes}), 200

@routes.route('/recipes/<int:id>', methods=['GET'])
def get_recipe(id):
    recipe = Recipe.query.filter_by(id=id).first()
    if recipe:
        return jsonify(recipe.to_dict()), 200
    else:
        return {"message": "Recipe not found"}, 404

@routes.route('/recipes/<int:id>', methods=['PUT'])
@jwt_required(optional=True)  # JWT token is optional for updating recipes
def update_recipe(id):
    try:
        data = request.get_json()
        recipe = Recipe.query.filter_by(id=id).first()
        if recipe:
            recipe.title = data['title']
            recipe.ingredients = data['ingredients']
            recipe.instructions = data['instructions']
            recipe.servings = data['servings']
            recipe.prep_time = data.get('prep_time')
            recipe.cook_time = data.get('cook_time')
            recipe.cuisine = data.get('cuisine')
            recipe.difficulty = data.get('difficulty')
            db.session.commit()
            return {"message": "Recipe updated successfully"}, 200
        else:
            return {"message": "Recipe not found"}, 404
    except IntegrityError:
        db.session.rollback()
        return {"message": "Recipe could not be updated. The data provided is not valid."}, 400

@routes.route('/recipes/<int:id>', methods=['DELETE'])
@jwt_required(optional=True)  # JWT token is optional for deleting recipes
def delete_recipe(id):
    recipe = Recipe.query.filter_by(id=id).first()
    if recipe:
        db.session.delete(recipe)
        db.session.commit()
        return {"message": "Recipe deleted"}, 200
    else:
        return {"message": "Recipe not found"}, 404
