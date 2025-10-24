from flask_jwt_extended import jwt_required
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema


blp = Blueprint("Items", __name__, description="Operation on items")


@blp.route("/item/<int:item_id>")
class Item(MethodView): # See Individual Items
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    @jwt_required()
    def delete(self, item_id): # Delete An Item
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted."}

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    @jwt_required()
    def put(self, item_data, item_id): # Edit Individual Item
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item


    
@blp.route("/item")
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        
        try:
            db.session.add(item)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(400, message="Constraint violation (duplicate name or invalid store_id).")
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="Database error while inserting item.")

        return item



    
