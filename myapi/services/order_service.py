from datetime import datetime
from myapi.models import db, Order, OrderStatus, Cart, CartItem, UserItem, Transaction, TransactionStatus

class OrderService:
    """Service class to handle all order-related operations."""

    @staticmethod
    def create_order(user, cart, total_price, currency="USD"):
        """
        Create an order from the provided cart.
        - Marks the cart as converted.
        - Adds an entry to the `Order` table.
        - Returns the created order.
        """
        if not cart.items:
            raise ValueError("Cart is empty. Cannot create an order.")

        # Create the order
        order = Order(
            user_id=user.id,
            total_price=total_price,
            currency=currency,
            status=OrderStatus.PENDING
        )
        db.session.add(order)

        # Link cart items to the order and add them to UserItem
        for item in cart.items:
            UserItem(
                user_id=user.id,
                product_id=item.product_id,
                order_id=order.id,
                downloads=0,
                rating=None
            )
        
        # Update the cart's status
        cart.status = Cart.Status.CONVERTED
        db.session.commit()

        return order

    @staticmethod
    def mark_order_paid(order, transaction_id=None):
        """
        Marks the order as paid and links it to a successful transaction.
        """
        if order.status != OrderStatus.PENDING:
            raise ValueError("Order is not in a payable state.")

        order.status = OrderStatus.PAID
        order.paid_at = datetime.utcnow()

        # Optional: Link transaction
        if transaction_id:
            transaction = Transaction.query.get(transaction_id)
            if transaction and transaction.status == TransactionStatus.COMPLETED:
                order.transaction_id = transaction.id

        db.session.commit()

    @staticmethod
    def cancel_order(order):
        """
        Cancel an order and mark the cart as active again.
        """
        if order.status not in [OrderStatus.PENDING, OrderStatus.PAID]:
            raise ValueError("Only pending or paid orders can be canceled.")

        order.status = OrderStatus.CANCELED
        order.canceled_at = datetime.utcnow()

        # Reactivate the cart
        cart = Cart.query.get(order.cart_id)
        if cart:
            cart.status = Cart.Status.ACTIVE

        db.session.commit()

    @staticmethod
    def add_cart_items_to_user_items(user, cart, order):
        """
        Add items from the cart to the `UserItem` table for a given order.
        """
        for cart_item in cart.items:
            user_item = UserItem(
                user_id=user.id,
                product_id=cart_item.product_id,
                order_id=order.id,
                downloads=0,
                rating=None
            )
            db.session.add(user_item)
        
        db.session.commit()

    @staticmethod
    def get_order_details(order_id):
        """
        Fetch detailed information about an order.
        """
        order = Order.query.get(order_id)
        if not order:
            raise ValueError("Order not found.")

        return {
            "id": order.id,
            "user_id": order.user_id,
            "total_price": order.total_price,
            "currency": order.currency,
            "status": order.status.value,
            "created_at": order.created_at.isoformat(),
            "paid_at": order.paid_at.isoformat() if order.paid_at else None,
            "items": [item.to_dict() for item in order.items]
        }
