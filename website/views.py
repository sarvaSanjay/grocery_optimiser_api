from flask import Blueprint, request, jsonify
from . import db
from .scraper import get_data
from .models import Orders
from .optimiser import cheapest_list
import threading

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
def index():
    return 'Hello'
@views.route('/order', methods=['POST'])
def order():
    data = request.get_json()
    session_id = data['session_id']
    orders = Orders.query.filter_by(user_id=session_id).all()
    if not orders:
        return jsonify(message='Not a previous user', category='not found')
    
    shopping_list = []
    for item in orders:
        order = {
            'name': item.item,
            'number': item.number,
            'units': item.unit,
            'estimated_cost': item.estimated_price
        }
        shopping_list.append(order)
    return jsonify(order=shopping_list)

def nofrills_data(data, item_name):
    data[0] = get_data(0, item_name)
def loblaws_data(data, item_name):
    data[1] = get_data(1, item_name)
def metro_data(data, item_name):
    data[2] = get_data(2, item_name)

@views.route('/addorder', methods=['POST'])
def add_order():
    data = request.get_json()
    item_name = data['name']
    user_id = data['session_id']
    number = data['number']

    datan = [0, 1, 2]
    x = threading.Thread(target=nofrills_data, args=(datan, item_name))
    y = threading.Thread(target=loblaws_data, args=(datan, item_name))
    z = threading.Thread(target=metro_data, args=(datan, item_name))
    x.start()
    y.start()
    z.start()
    x.join()
    y.join()
    z.join()

    total_data = datan[2] + datan[1] + datan[0]
    possible_units = {}
    sum_cost = 0

    for item in total_data:
        possible_units[item['units']] = possible_units.get(item['units'], 0) + 1
        sum_cost += item['price']
    average_cost = sum_cost / len(total_data)
    if '100g' in possible_units and '100ml' in possible_units:
        if possible_units['100g'] >= possible_units['100ml']:
            max_units = 'g'
        else:
            max_units = 'ml'
    elif '100g' in possible_units:
        max_units = 'g'
    else:
        max_units = 'ml'
    order = Orders(user_id= user_id, item= item_name, number= number, unit= max_units, estimated_price= round(average_cost, 2))
    db.session.add(order)
    db.session.commit()
    return jsonify(unit=max_units, estimated_price=order.estimated_price)
    
@views.route('/edit', methods=['POST'])
def edit():
    data = request.get_json()
    user_id = data['session_id']
    quantity = data['quantity']
    item = data['name']
    order = Orders.query.filter_by(user_id=user_id, item=item).first()
    order.number = quantity
    db.session.commit()
    return jsonify(message='edited', category='success') #problem: you need to update the lowest price

@views.route('/delete', methods=['POST'])
def delete_order():
    data = request.get_json()
    user_id = data['session_id']
    item = data['name']
    Orders.query.filter_by(user_id=user_id, item=item).delete()
    db.session.commit()
    return jsonify(message='Deleted!', category='success')

@views.route('/optimize', methods=['POST'])
def optimise():
    data1 = request.get_json()
    user_id = data1['session_id']
    orders = Orders.query.filter_by(user_id=user_id).all()
    shops = ['NoFrills', 'LobLaws', 'Metro']
    result_data = {}
    cheap_prices = {}
    quantity_map = {}
    for order in orders:
        quantity_map[order.item] = order.number
    for i in range(3):
        data = {}
        for order in orders:
            data[order.item] = get_data(i, order.item)
        result_data[shops[i]], cheap_prices[shops[i]] = cheapest_list(data, quantity_map)
    for shop in shops:
        if cheap_prices[shop] == min(cheap_prices.values()):
            winner = shop

    
    return jsonify(winner= winner, shopping_lists= result_data)