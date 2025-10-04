from sqlalchemy import inspect
from app import app, db
from models import User, Shipment  

def main():
    with app.app_context():
        db.create_all()
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print("Tables currently in database:", tables)

if __name__ == "__main__":
    main()