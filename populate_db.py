# populate_db.py
from paperbookcollections.models import Product
from paperbookcollections import create_app

# Create the Flask app
app = create_app()

# Populate the database with initial products
def populate_db():
    with app.app_context():
        # Add your database population logic here...
        pass

if __name__ == '__main__':
    populate_db()
