# Student Management System

## Prerequisites
Ensure you have the following installed:
- **Python 3.11+**
- **PostgreSQL**
- **pip** (Python package manager)

## Setup Instructions

### 1. Clone the Repository
```sh
git clone https://github.com/Aliza05/studentManagementSystemBackend.git
```

### 2. Create and Activate a Virtual Environment
```sh
python -m venv venv  # Create virtual environment
source venv/bin/activate  # Activate on macOS/Linux
venv\Scripts\activate  # Activate on Windows
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Configure Database (PostgreSQL)
Create a new PostgreSQL database and user.

#### 4.1 Create a `.env` File
Create a `.env` file in the project root (sample env file is in the project for reference) and add the following details:

```ini
# Database Configuration
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Apply Database Migrations
```sh
python manage.py migrate
```

### 6. Seed Initial Data
```sh
python manage.py seed_data
```

### 7. Run the Development Server
```sh
python manage.py runserver
```

### 8. Create Super User
Create superuser and access it the Django Admin on url `http://127.0.0.1:8000/admin`
```sh
python manage.py createsuperuser
```

### 9. Run Tests
```sh
python manage.py test
```
Following TestCases have been covered:
#	Test Case	Expected Outcome
✅ 1	Create a valid student	201 Created
❌ 2	Create student with invalid email	400 Bad Request
❌ 3	Create student under 18	400 Bad Request
✅ 4	Get list of students	200 OK
✅ 5	Create a valid course	201 Created
❌ 6	Create course with invalid credits	400 Bad Request
✅ 7	Get list of courses	200 OK
✅ 8	Create a valid enrollment	201 Created
❌ 9	Create duplicate enrollment	400 Bad Request
✅ 10	Get enrollment stats	200 OK


## API Endpoints
Once the server is running, access the API at:
```
http://127.0.0.1:8000/
```

## Troubleshooting
- If migrations fail, ensure PostgreSQL is running and the `.env` file has correct values.
- If dependencies are missing, re-run:
  ```sh
  pip install -r requirements.txt
  ```
