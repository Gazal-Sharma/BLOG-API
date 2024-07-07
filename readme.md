# Blog API

The Blog API is a Flask-based API for managing blog posts, comments, and user authentication. It provides use of CRUD operations (CREATE, READ, UPDATE, DELETE) on blog posts, comments and user details as well,

## Table of Contents

- [Features](#features)
- [Packages Used](#packages-used)
- [Setup Instructions](#setup-instructions)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [Folder Structure](#folder-structure)
- [Contribution](#contribution)
## Features

- User authentication -- user registration and login functionality -- (login, signup)
- CRUD operations for blog posts
- Commenting on blog posts, CRUD operations on blog posts
- Swagger documentation for APIs
- database Setup using PostgreSQL

## Packages Used

- **Flask**: Python web framework
- **Swagger/OpenAPI**: Used for API documentation.
- **Psycopg2**: PostgreSQL adapter for Python
- **Flask-Login**: Manages user sessions and authentication.
- **SQLAlchemy**: SQL toolkit and ORM for Python
- **Flask-Bcrypt**: Password hashing library
- **Git**: Version control
- **GitHub**: Remote repository hosting
- **Other Dependencies**: Jinja2, Werkzeug, SQLAlchemy, and various utility libraries as per project needs.

## Setup Instructions

### Prerequisites

- Python 3.6 or higher
- PostgreSQL installed and running locally or remote connection details
- Git installed
- API testing tool (e.g., Postman)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Gazal-Sharma/BLOG-API.git
   cd BLOG-API
   ```

2. **Create a virtual environment (optional but recommended)**

    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment**

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On macOS and Linux:

        ```bash
        source venv/bin/activate
        ```

4. **Install the required dependencies**

    ```bash
    pip3 install -r requirements.txt
    ```

### Running the Application

1. **Set up the database**

    Ensure that your database is set up and the connection details are correctly configured in `db_run.py`. 
    Set up a create_tables function in db_run.py which creates table using the SQL scripts in `sql_table.sql`.

2. **Run the application**

    ```bash
    python db_run.py
    ```

    This will start the application and set up the necessary database connections.

3. **Access the application**

    Once the application is running, you can access it via your web browser. The exact URL and port will depend on how the application is configured.

4. **API Documentation**

    The API documentation is available through Swagger. You can access it by navigating to the `/swagger.yaml` endpoint in your running application.

---

For detailed information on each blueprint and its functionality, refer to the documentation within each subdirectory under `blog/blueprints/`.

For detailed information on each relationship between table attributes and their functionality, refer to the documentation within each subdirectory under `blog/data_models/`.

If you encounter any issues during setup or while running the application, please check the issues page on the repository or contact the maintainer.




## Project Structure
The project directory structure includes:
- **db_run.py**:Main entry point of Flask. Configures and connects to the PostgreSQL database, creates tables and runs Flask app
- **blueprints/**: Contains separate modules for blog posts, comments, user details, each as Flask blueprints.
- **data_models/**: Contains data models for blogposts, comments and user details
- **sql_table.sql**: Contains Queries for creating Tables
- **requirements.txt**: Lists all Python dependencies for the project.
- **swagger.yaml**: Contains OpenAPI documentation

## Folder Structure
EDC-Project/
    ├── blog/
    │   ├── blueprints/
    │   │   ├── blogpost/
    │   │   │   ├── blogpost.py   # Blog post routes and logic
    │   │   ├── comments/
    │   │   │   ├── comments.py   # Comment routes and logic
    │   │   ├── user_details/
    │   │   │   ├── user.py       # User routes and logic
    │   ├── data_models/
    │   │   ├── __init__.py       # Initialization for data models
    │   │   ├── blogpost.py       # Blog post data model
    │   │   ├── comments.py       # Comments data model
    │   │   ├── user.py           # User data model
    │   │
    │   ├── db_run.py                 # Database connection and setup
    │   ├── sql_table.sql             # SQL table definitions
    │
    ├── blogapi/
    │   ├── swagger.yaml          # Swagger API documentation
    ├── venv/                     # Virtual environment
    ├── readme.md                 # Project documentation
    ├── requirements.txt          # Python dependencies

## Contributions

Contributions are welcome! Fork the repository, create a branch, commit changes, and open a pull request.