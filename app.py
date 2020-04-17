from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from db import db


from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemsList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myhmdata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'myhmsecret'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity) # *** !!! /auth !!! ***

api.add_resource(UserRegister, '/register')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemsList, '/items')         # DONE BY ME

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

db.init_app(app)

if __name__ == '__main__':

    app.run(port=5999, debug=True)   # NOTE: "port=5000" is the DEFAULT, set debugging
