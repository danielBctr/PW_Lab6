from database.db import db

class Recipe(db.Model):
    __tablename__ = 'recipe'
    pk = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.String(1000), nullable=False)
    instructions = db.Column(db.String(2000), nullable=False)
    servings = db.Column(db.Integer, nullable=False)
    prep_time = db.Column(db.String(50))
    cook_time = db.Column(db.String(50))
    cuisine = db.Column(db.String(100))
    difficulty = db.Column(db.String(50))

    def to_dict(self):
        return {
            "pk": self.pk,
            "id": self.id,
            "title": self.title,
            "ingredients": self.ingredients,
            "instructions": self.instructions,
            "servings": self.servings,
            "prep_time": self.prep_time,
            "cook_time": self.cook_time,
            "cuisine": self.cuisine,
            "difficulty": self.difficulty
        }
