import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id."
    )


    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):            # Keep same signature than get method for having same endpoint
        if ItemModel.find_by_name(name):
            return {'messsage': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        #item = {'name': name, 'price': data['price']}
        item = ItemModel(name, data['price'], data['store_id']) # Change as an OBJECT
                                                                # can be (name, **data)
        try:
            #ItemModel.insert(item)
            item.save_to_db()          # Because item is now an OBJECT
        except:
            return {"message": "An error occured inserting the item."}, 500 # *** Internal Server Error ***

        #return item, 201             # "Status code": 201 (object have been created)
        return item.json(), 201       ## .json() now it is an OBJECT

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item delete'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)                     ## Existing "item"

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()

        return item.json()               # Turn it to a DICTIONARY


class ItemsList(Resource):           # DONE BY ME
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]} # ** !!! By ME !!! **
        #Possible with lambda function: return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
