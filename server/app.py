#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    return jsonify([bakery.to_dict() for bakery in bakeries]) 

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = db.session.get(Bakery, id)  #  Updated method
    if not bakery:
        return jsonify({"error": "Bakery not found"}), 404
    
    return jsonify({
        "id": bakery.id,
        "name": bakery.name,
        "created_at": bakery.created_at.strftime('%Y-%m-%d %H:%M:%S'),  #  Ensure created_at is formatted
        "baked_goods": [baked_good.to_dict() for baked_good in bakery.baked_goods]
    })

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    if not baked_goods:
        return jsonify({"error": "Baked goods not found"}), 404
    return jsonify([baked_good.to_dict() for baked_good in baked_goods])  #  Fix JSON format

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    
    if not baked_good:
        return jsonify({"error": "Baked goods not found"}), 404
    
    return jsonify(baked_good.to_dict())  

if __name__ == '__main__':
    app.run(port=5555, debug=True)
