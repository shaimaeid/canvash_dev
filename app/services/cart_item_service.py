from app.models import db, CartItem

class CartItemService:
    @staticmethod
    def create_cart_item(cart_id, product_id, quantity):
        new_cart_item = CartItem(cart_id=cart_id, product_id=product_id, quantity=quantity)
        db.session.add(new_cart_item)
        db.session.commit()
        return new_cart_item

    @staticmethod
    def get_cart_item_by_id(cart_item_id):
        return CartItem.query.get(cart_item_id)

    @staticmethod
    def update_cart_item(cart_item_id, cart_id, product_id, quantity):
        cart_item = CartItem.query.get(cart_item_id)
        if not cart_item:
            return None
        cart_item.cart_id = cart_id
        cart_item.product_id = product_id
        cart_item.quantity = quantity
        db.session.commit()
        return cart_item

    @staticmethod
    def delete_cart_item(cart_item_id):
        cart_item = CartItem.query.get(cart_item_id)
        if not cart_item:
            return None
        db.session.delete(cart_item)
        db.session.commit()
        return cart_item