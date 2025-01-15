from myapi.models import db, Cart, CartItem, User

class CartService:
    @staticmethod
    def create_cart(user_id):
        new_cart = Cart(user_id=user_id)
        db.session.add(new_cart)
        db.session.commit()
        return new_cart

    @staticmethod
    def get_all_carts():
        return Cart.query.all()

    @staticmethod
    def get_cart_by_id(cart_id):
        return Cart.query.get(cart_id)

    @staticmethod
    def update_cart(cart_id, user_id):
        cart = Cart.query.get(cart_id)
        if not cart:
            return None
        cart.user_id = user_id
        db.session.commit()
        return cart

    @staticmethod
    def delete_cart(cart_id):
        cart = Cart.query.get(cart_id)
        if not cart:
            return None
        db.session.delete(cart)
        db.session.commit()
        return cart

    @staticmethod
    def add_to_cart(user_id, product_id, quantity=1):
        user = User.query.get(user_id)
        if not user:
            return None
        cart = user.carts[-1] if user.carts else None
        if not cart:
            cart = CartService.create_cart(user_id)
        
        cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
            db.session.add(cart_item)
        
        db.session.commit()
        return cart_item