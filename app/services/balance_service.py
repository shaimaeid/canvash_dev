from app.models import db, User, Transaction, TransactionType, TransactionStatus
from datetime import datetime


class InsufficientBalanceError(Exception):
    """Exception raised when a user does not have enough balance."""
    pass


class BalanceService:
    """Service class for managing user balances and transactions."""

    @staticmethod
    def get_balance(user_id):
        """
        Get the current balance of a user.
        """
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found.")

        return user.balance

    @staticmethod
    def add_funds(user_id, amount, currency="USD", method=TransactionType.CASH, reference_id=None):
        """
        Add funds to the user's balance.
        Creates a transaction record.
        """
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found.")

        # Update user balance
        user.balance += amount

        # Record the transaction
        transaction = Transaction(
            user_id=user_id,
            amount=amount,
            currency=currency,
            method=method,
            source="balance_topup",  # Indicating this is a top-up
            status=TransactionStatus.COMPLETED,
            reference_id=reference_id,
            created_at=datetime.utcnow()
        )
        db.session.add(transaction)
        db.session.commit()

        return transaction

    @staticmethod
    def deduct_funds(user_id, amount, currency="USD", reason="purchase", reference_id=None):
        """
        Deduct funds from the user's balance.
        Creates a transaction record.
        """
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found.")

        if user.balance < amount:
            raise InsufficientBalanceError("User does not have enough balance.")

        # Deduct from user balance
        user.balance -= amount

        # Record the transaction
        transaction = Transaction(
            user_id=user_id,
            amount=-amount,  # Negative amount for deduction
            currency=currency,
            method=TransactionType.BALANCE,
            source=reason,
            status=TransactionStatus.COMPLETED,
            reference_id=reference_id,
            created_at=datetime.utcnow()
        )
        db.session.add(transaction)
        db.session.commit()

        return transaction

    @staticmethod
    def refund(user_id, amount, currency="USD", reference_id=None):
        """
        Refund funds to the user's balance.
        Creates a transaction record.
        """
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found.")

        # Update user balance
        user.balance += amount

        # Record the transaction
        transaction = Transaction(
            user_id=user_id,
            amount=amount,
            currency=currency,
            method=TransactionType.REFUND,
            source="refund",
            status=TransactionStatus.COMPLETED,
            reference_id=reference_id,
            created_at=datetime.utcnow()
        )
        db.session.add(transaction)
        db.session.commit()

        return transaction

    @staticmethod
    def get_transaction_history(user_id, limit=10):
        """
        Retrieve a user's transaction history.
        """
        transactions = Transaction.query.filter_by(user_id=user_id).order_by(
            Transaction.created_at.desc()
        ).limit(limit).all()

        return [t.to_dict() for t in transactions]
