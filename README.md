# shipsy-assignment
**Live demo:** [https://<your-render-url>](https://shipment-tracker-in2u.onrender.com/)  
**Repo:** [https://github.com/<your-username>/<your-repo>](https://github.com/SomyaAggarwal1209/shipsy-assignment)
This is a web application for managing shipments, built with the **Flask** framework in Python. 
It allows users to register and log in to manage a list of shipments.
Key features include:
*   **User Authentication**: It has a complete user authentication system using **Flask-Login**, allowing users to register, log in, and log out. Routes that manage shipments are protected and require a user to be logged in.
*   **Full CRUD Functionality**: The application implements all four CRUD (Create, Read, Update, Delete) operations for shipments:
*   **Create**: Users can add new shipments with details like description, status, cost, and fragility.
*   **Read**: It displays a paginated list of all shipments, which can be filtered by status (e.g., Pending, In-Transit, Delivered). Users can also view the details of a single shipment.
*   **Update**: Existing shipments can be edited.
*   **Delete**: Shipments can be removed from the system.
**Database**: The application uses **Flask-SQLAlchemy** as an ORM to interact with a **SQLite** database (`shipsy.db`). It defines two main database models: `User` and `Shipment`.
**Calculated Fields**: The `Shipment` model includes a calculated `total_cost` property, which is dynamically computed from the base cost, tax rate, and handling fee.
*   **Configuration**: It uses a `.env` file to manage configuration settings like the application's secret key.
The main application logic, routes, and database models are defined in `app.py`, and it renders HTML from the `templates/` directory. The `openapi.yaml` file suggests that it may also be designed to expose a RESTful API.

## Tech stack
- Python 3.11+  
- Flask, Flask-Login, Flask-SQLAlchemy  
- MySQL optional (SQLAlchemy used with SQLite by default)  
- Bootstrap 5 for UI  
- Gunicorn & Waitress (dev)  
- Deployed on Render

## Live demo
Open the app: `[https://<your-render-url>](https://shipment-tracker-in2u.onrender.com/)`  
Swagger/OpenAPI UI: `[https://<your-render-url>/api-docs](https://shipment-tracker-in2u.onrender.com/api-docs)`

## Quickstart (local)
```bash
# create & activate venv
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

# install
pip install -r requirements.txt

# set secret (do not commit .env)
export SECRET_KEY="your_secret_here"        # or set in .env on Windows
# run
python app.py
# or (production-like) with waitress (Windows)
python -m waitress --port=8000 wsgi:application
