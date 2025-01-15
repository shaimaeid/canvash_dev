import random
from app import create_app
from myapi.models import db, Product, Category, User, Cart, CartItem
from myapi.logger import mylogger

def drop_and_create_tables():
    app = create_app()
    with app.app_context():
        try:
            db.drop_all()
            db.create_all()
            mylogger.info("Tables dropped and recreated successfully.")
        except Exception as e:
            mylogger.error(f"Error dropping and recreating tables: {str(e)}")
            raise

def seed_categories():
    app = create_app()
    with app.app_context():
        try:
            categories = [
                Category(name="Graphics", description="Graphic design templates", slug="graphics", icon="fa-graphics"),
                Category(name="Stationaries", description="Stationary templates", slug="stationaries", icon="fa-stationaries"),
                Category(name="Presentation Templates", description="Templates for presentations", slug="presentation-templates", icon="fa-presentation")
            ]
            db.session.bulk_save_objects(categories)
            db.session.commit()
            mylogger.info("Categories seeded successfully.")
            return categories
        except Exception as e:
            db.session.rollback()
            mylogger.error(f"Error seeding categories: {str(e)}")
            raise

def seed_users():
    app = create_app()
    with app.app_context():
        try:
            users = [
                User(username="admin", email="admin@example.com", password="password", role=User.ADMIN),
                User(username="subscriber", email="subscriber@example.com", password="password", role=User.SUBSCRIBER),
                User(username="designer", email="designer@example.com", password="password", role=User.DESIGNER)
            ]
            db.session.bulk_save_objects(users)
            db.session.commit()
            mylogger.info("Users seeded successfully.")
            return users
        except Exception as e:
            db.session.rollback()
            mylogger.error(f"Error seeding users: {str(e)}")
            raise

def seed_products():
    app = create_app()

    with app.app_context():
        categories = Category.query.all()
        try:
            category_ids = [category.id for category in categories]
            designer_id = 3 # make sure you run user seed before product seed
            mylogger.info(f"Category IDs: {category_ids}")
            mylogger.info(f"Designer ID: {designer_id}")

            products = [
                Product(title="Business Card Template", description="Professional business card template", price=10.00, category_id=random.choice(category_ids), designer_id=designer_id),
                Product(title="Flyer Template", description="Creative flyer template", price=15.00, category_id=random.choice(category_ids), designer_id=designer_id),
                Product(title="Logo Template", description="Modern logo template", price=20.00, category_id=random.choice(category_ids), designer_id=designer_id),
                Product(title="Letterhead Template", description="Elegant letterhead template", price=12.00, category_id=random.choice(category_ids), designer_id=designer_id),
                Product(title="Envelope Template", description="Stylish envelope template", price=8.00, category_id=random.choice(category_ids), designer_id=designer_id),
                Product(title="Notebook Template", description="Customizable notebook template", price=18.00, category_id=random.choice(category_ids), designer_id=designer_id),
                Product(title="PowerPoint Presentation Template", description="Creative PowerPoint presentation template", price=15.00, category_id=random.choice(category_ids), designer_id=designer_id),
                Product(title="Keynote Presentation Template", description="Professional Keynote presentation template", price=17.00, category_id=random.choice(category_ids), designer_id=designer_id),
                Product(title="Google Slides Template", description="Modern Google Slides presentation template", price=14.00, category_id=random.choice(category_ids), designer_id=designer_id),
                Product(title="Brochure Template", description="Elegant brochure template", price=22.00, category_id=random.choice(category_ids), designer_id=designer_id)
            ]
            db.session.bulk_save_objects(products)
            db.session.commit()
            mylogger.info("Products seeded successfully.")
            return products
        except Exception as e:
            db.session.rollback()
            mylogger.error(f"Error seeding products: {str(e)}")
            raise

def seed_carts():
    app = create_app()
    with app.app_context():
        try:
            subscriber_id = 2
            mylogger.info(f"Subscriber ID: {subscriber_id}")

            carts = [
                Cart(user_id=subscriber_id)
            ]
            db.session.bulk_save_objects(carts)
            db.session.commit()
            mylogger.info("Carts seeded successfully.")
            return carts
        except Exception as e:
            db.session.rollback()
            mylogger.error(f"Error seeding carts: {str(e)}")
            raise

def seed_cart_items():
    app = create_app()

    with app.app_context():
        products = Product.query.all()
        cart = Cart.query.filter_by(user_id=2).first()
        try:
            cart_id = cart.id
            product_ids = [product.id for product in products]
            mylogger.info(f"Cart ID: {cart_id}")
            mylogger.info(f"Product IDs: {product_ids}")

            cart_items = [
                CartItem(cart_id=cart_id, product_id=random.choice(product_ids), quantity=1),
                CartItem(cart_id=cart_id, product_id=random.choice(product_ids), quantity=2),
                CartItem(cart_id=cart_id, product_id=random.choice(product_ids), quantity=3)
            ]
            db.session.bulk_save_objects(cart_items)
            db.session.commit()
            mylogger.info("Cart items seeded successfully.")
        except Exception as e:
            db.session.rollback()
            mylogger.error(f"Error seeding cart items: {str(e)}")
            raise

if __name__ == "__main__":
    #drop_and_create_tables()    
    # users = seed_users()
    # categories = seed_categories()
    products = seed_products()
    carts = seed_carts()
    seed_cart_items()
