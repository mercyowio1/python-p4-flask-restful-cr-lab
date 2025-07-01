from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from models import db, Plant

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def home():
    return '<h1>Plant Store API</h1>'

# Index Route - GET all plants
@app.route('/plants', methods=['GET'])
def get_plants():
    plants = Plant.query.all()
    plants_serialized = [plant.to_dict() for plant in plants]
    return make_response(plants_serialized, 200)

# Show Route - GET one plant
@app.route('/plants/<int:id>', methods=['GET'])
def get_plant(id):
    plant = Plant.query.get_or_404(id)
    return make_response(plant.to_dict(), 200)

# Create Route - POST a new plant
@app.route('/plants', methods=['POST'])
def create_plant():
    data = request.get_json()

    new_plant = Plant(
        name=data['name'],
        image=data['image'],
        price=data['price']
    )

    db.session.add(new_plant)
    db.session.commit()

    return make_response(new_plant.to_dict(), 201)

if __name__ == '__main__':
    app.run(port=5555)