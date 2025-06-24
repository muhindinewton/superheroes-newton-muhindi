# Superheroes API

This project implements a Flask API for tracking heroes and their superpowers.

## Features

* **RESTful Endpoints:** Provides endpoints for managing heroes, powers, and the relationships between them.
* **Database Management:** Utilizes SQLAlchemy for object-relational mapping (ORM) and Flask-Migrate for database schema management.
* **Data Models:** Defines `Hero`, `Power`, and `HeroPower` models with appropriate relationships and cascading deletes.
* **Data Validation:** Implements validation rules for `HeroPower` strength and `Power` description.
* **Serialization:** Configures serialization rules to manage recursion depth in JSON responses.

## Data Models

The API interacts with the following data models:

* **`Hero`**: Represents a superhero.
    * `id` (Primary Key)
    * `name` (String)
    * `super_name` (String)
* **`Power`**: Represents a unique superpower.
    * `id` (Primary Key)
    * `name` (String)
    * `description` (String, validated: must be present and at least 20 characters long)
* **`HeroPower`**: A join table representing the strength of a hero's specific power.
    * `id` (Primary Key)
    * `strength` (String, validated: must be 'Strong', 'Weak', or 'Average')
    * `hero_id` (Foreign Key to `Hero.id`, with `ondelete='CASCADE'`)
    * `power_id` (Foreign Key to `Power.id`, with `ondelete='CASCADE'`)

**Relationships:**

* A `Hero` has many `Power`s through `HeroPower`.
* A `Power` has many `Hero`s through `HeroPower`.
* A `HeroPower` belongs to a `Hero` and belongs to a `Power`.
* `HeroPower` is configured to cascade deletes, meaning if a Hero or Power is deleted, associated `HeroPower` records will also be deleted.

## Setup Instructions

Follow these steps to get the project up and running:

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd superheroes-firstname-lastname # Replace with your actual repo name
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Initialize and run database migrations:**
    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

5.  **Seed the database:**
    ```bash
    python seed.py
    ```
    This script will populate your database with initial dummy data.

6.  **Run the Flask application:**
    ```bash
    flask run -p 5555
    ```
    The API will be accessible at `http://localhost:5555`.

## API Endpoints

The following endpoints are available:

| HTTP Method | Endpoint                 | Description                                                        | Request Body (Example)                               | Response Body (Example)                                                                                                                                                                                                                                                                          |
| :---------- | :----------------------- | :----------------------------------------------------------------- | :--------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `GET`       | `/heroes`                | Get a list of all heroes.                                          | N/A                                                  | `[{"id": 1, "name": "Kamala Khan", "super_name": "Ms. Marvel"}, ...]`                                                                                                                                                                                                                            |
| `GET`       | `/heroes/<int:id>`       | Get details for a specific hero, including their powers.           | N/A                                                  | `{ "id": 1, "name": "Kamala Khan", "super_name": "Ms. Marvel", "hero_powers": [{"hero_id": 1, "id": 1, "power": {"description": "gives the wielder the ability to fly through the skies at supersonic speed", "id": 2, "name": "flight"}, "power_id": 2, "strength": "Strong"}]}` (or `{"error": "Hero not found"}` if not found) |
| `GET`       | `/powers`                | Get a list of all powers.                                          | N/A                                                  | `[{"description": "gives the wielder super-human strengths", "id": 1, "name": "super strength"}, ...]`                                                                                                                                                                                           |
| `GET`       | `/powers/<int:id>`       | Get details for a specific power.                                  | N/A                                                  | `{"description": "gives the wielder super-human strengths", "id": 1, "name": "super strength"}` (or `{"error": "Power not found"}` if not found)                                                                                                                                                     |
| `PATCH`     | `/powers/<int:id>`       | Update the description of an existing power.                       | `{"description": "Valid Updated Description"}`       | `{"description": "Valid Updated Description", "id": 1, "name": "super strength"}` (200 OK) or `{"error": "Power not found"}` (404) or `{"errors": ["validation errors"]}` (400)                                                                                                                          |
| `POST`      | `/hero_powers`           | Create a new association between a hero and a power with a strength. | `{"strength": "Average", "power_id": 1, "hero_id": 3}` | `{ "id": 11, "hero_id": 3, "power_id": 1, "strength": "Average", "hero": {"id": 3, "name": "Gwen Stacy", "super_name": "Spider-Gwen"}, "power": {"description": "gives the wielder super-human strengths", "id": 1, "name": "super strength"}}` (201 Created) or `{"errors": ["validation errors"]}` (400/404) |

## Error Handling

* **404 Not Found**:
    * Returned for `GET /heroes/<id>` if the hero does not exist.
    * Returned for `GET /powers/<id>` or `PATCH /powers/<id>` if the power does not exist.
    * Returned for `POST /hero_powers` if the `hero_id` or `power_id` do not exist.
    ```json
    { "error": "Hero not found" }
    ```
    or
    ```json
    { "errors": ["Hero not found"] }
    ```
* **400 Bad Request**:
    * Returned for `PATCH /powers/<id>` if the new `description` fails validation (e.g., too short).
    * Returned for `POST /hero_powers` if the `strength` fails validation (not 'Strong', 'Weak', or 'Average').
    ```json
    { "errors": ["Description must be at least 20 characters long."] }
    ```
    or
    ```json
    { "errors": ["Strength must be one of: Strong, Weak, Average."] }
    ```

## Technologies Used

* **Flask**: A lightweight Python web framework.
* **Flask-SQLAlchemy**: An extension for Flask that adds SQLAlchemy support, making it easy to interact with databases using ORM.
* **Flask-Migrate**: An extension that handles SQLAlchemy database migrations via Alembic.
* **Flask-RESTful**: A Flask extension for rapidly building REST APIs.
* **SQLAlchemy-Serializer**: Used for convenient serialization of SQLAlchemy model instances into dictionaries for JSON responses.
* **SQLite3**: The default relational database used for development.

## Author

* **Newton Muhindi**
    * [Newton Muhindi GitHub Profile Link] (e.g., `https://github.com/newtonmuhindi`)


## License

This project is licensed under the MIT License - see the `LICENSE` file (if you choose to create one) for details.