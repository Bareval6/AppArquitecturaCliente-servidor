# server.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from db import session, Equipment # type: ignore

app = Flask(__name__)
CORS(app)

@app.route('/api/equipment', methods=['GET'])
def get_equipment():
    equipment = session.query(Equipment).all()
    return jsonify([{
        'id': eq.id,
        'name': eq.name,
        'model': eq.model,
        'quantity': eq.quantity,
        'location': eq.location
    } for eq in equipment])

@app.route('/api/equipment', methods=['POST'])
def add_equipment():
    data = request.json
    new_equipment = Equipment(
        name=data['name'],
        model=data['model'],
        quantity=data['quantity'],
        location=data['location']
    )
    session.add(new_equipment)
    session.commit()
    return jsonify({'message': 'Equipment added successfully'}), 201

@app.route('/api/equipment/<int:id>', methods=['DELETE'])
def delete_equipment(id):
    equipment = session.query(Equipment).filter_by(id=id).first()
    if equipment:
        session.delete(equipment)
        session.commit()
        return jsonify({'message': 'Equipment deleted successfully'}), 200
    return jsonify({'message': 'Equipment not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
