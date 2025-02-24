# 🐾 Pawfect Planner  
A **micro-services** based pet management application designed to help pet owners **organize pet care, track vaccinations, set reminders**, and more.  
The project includes:  
- A **FastAPI-based backend** for pet data management.  
- A **React-based frontend** (currently in development).  
- **Microservices for modular functionality** (e.g., Gemini API integration).  
- **Docker support** for seamless deployment.

---

## 📌 Features
### 🔹 Backend
- **Pet Profiles** 🐶🐱: Manage detailed pet profiles with breed, age, weight, and health history.
- **Vaccination Tracking 💉**: Store vaccination records and upcoming vaccinations.
- **Reminders ⏰**: Set and manage reminders for vet visits, vaccinations, and medication schedules.
- **Health Check API 🏥**: Provides basic health-related insights via APIs.
- **ICS Calendar Export 📅**: Export reminders to `.ics` files for Google Calendar, Outlook, etc.
- **Dynamic Breed Information 🔍**: Fetch breed-related data from external APIs.
- **Local Vet Search 🏥**: Locate nearby veterinary clinics using Google Maps.
- **Security 🔐**: Implements secure authentication using JWT and bcrypt.
- **Microservices Architecture 🏗️**: Modular services for scalability and maintainability.
- **Dockerized 🐳**: Fully containerized for easy deployment.

### 🔹 Frontend (Work in Progress)
- **React-based UI 🎨**: A clean, user-friendly interface for managing pet data.
- **Interactive Reminders & Notifications 🔔**: reminders (ics files) will automatically renew, so you will never miss a treatment nor a vaccine again.

---

## 🛠️ Technologies Used
### Backend
- **FastAPI** (Python 3.12) - High-performance web framework for API development.
- **PostgreSQL** - Relational database for storing pet data securely.
- **SQLAlchemy** - ORM for database management.
- **bcrypt** - Secure password hashing.
- **Pydantic** - Data validation and serialization.
- **HTTPX** - Making external API requests.
- **Redis** (Optional) - Caching and session management.
- **ICS Library** - Export reminders to calendar-compatible formats.
- **Docker & Docker Compose** - Containerized environment for deployment.

### Frontend (Upcoming)
- **React** - User-friendly, responsive UI.
- **React Router** - For navigation.
- **Redux (or Zustand)** - State management.
- **Tailwind CSS** - Modern styling framework.

---

## ⚙️ Prerequisites
To run the project, ensure you have:

- **[Docker](https://docs.docker.com/get-docker/)** installed.
- **[Docker Compose](https://docs.docker.com/compose/install/)** installed.
- (For local development) **Python 3.12** installed.

---

## 🚀 Installation and Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/EASS-HIT-PART-A-2024-CLASS-VI/PawfectPlanner.git
cd PawfectPlanner

# 🐾 Pawfect Planner

A microservices-based pet care application.

## 2️⃣ Set Up Environment Variables

Before running the project, you need to configure environment variables.

1. Create a `.env` file in the **root directory**.
2. Add the following:

   ```plaintext
   DATABASE_URL=postgresql://postgres:password@db:5432/pawfectplanner
   SECRET_KEY=your-secret-key
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   GEMINI_API_KEY=your-gemini-api-key
   ```

   - **`DATABASE_URL`** - Connection string for PostgreSQL.
   - **`SECRET_KEY`** - Used for JWT authentication (choose a secure key).
   - **`ACCESS_TOKEN_EXPIRE_MINUTES`** - Token expiration time (default: 60 minutes).
   - **`GEMINI_API_KEY`** - API Key for Gemini integration.

   Replace the placeholder values with your actual credentials.

## 🐳 Running the Project with Docker

### Start the Full Application

Use **Docker Compose** to run all services, including the backend, database, and external API integrations.

Build and start the containers:

```bash
docker-compose up --build
```

### Access the Backend API:

- **FastAPI Server:** [`http://localhost:8000`](http://localhost:8000)
- **Swagger API Documentation (Auto-Generated):** [`http://localhost:8000/docs`](http://localhost:8000/docs)
- **ReDoc API Docs:** [`http://localhost:8000/redoc`](http://localhost:8000/redoc)

### (Upcoming) Frontend UI:

- **React Frontend (Planned):** [`http://localhost:3000`](http://localhost:3000)

## 🗄️ Project Structure

This project follows a **modular microservices approach** with separate directories for the backend, frontend, and services.

```
PawfectPlanner/
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   │   ├── breeds.py
│   │   │   ├── healthcheck.py
│   │   │   ├── pets.py
│   │   │   ├── reminders.py
│   │   │   ├── treatments.py
│   │   │   ├── vet_search.py
│   │   ├── vaccines/
│   │   │   ├── cat_vaccines.json
│   │   │   ├── dog_vaccines.json
│   │   │   └── vaccines.py
│   │   ├── auth.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── security.py
│   │   ├── util.py
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
├── frontend/ (Upcoming)
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   ├── package.json
│   ├── vite.config.js
│   ├── README.md
├── docker-compose.yml
└── README.md
```

### 📌 Key Directories:

- **`backend/app/routes/`** → Contains all API endpoints.
- **`backend/app/vaccines/`** → Stores JSON data for vaccination schedules.
- **`backend/app/models.py`** → Defines database models using SQLAlchemy.
- **`backend/app/main.py`** → The entry point for FastAPI.
- **`frontend/src/`** → (Upcoming) Will contain React components for UI.

## ✅ Running Tests

To ensure the project runs correctly, use `pytest` to test the backend.

### Run tests locally:

```bash
pytest
```

### Run tests inside the Docker container:

```bash
docker exec -it pawfect-planner_app_1 pytest
```

## 🛠️ Development Notes

    ## Development Notes
    - All dependencies are listed in `requirements.txt`.
    - Use **Swagger UI** (`http://localhost:8000/docs`) for testing API endpoints during development.

    ---

    ## Contribution Guidelines
    1. Fork the repository.
    2. Create a new branch for your feature:
       ```bash
       git checkout -b feature-name
       ```
    3. Make your changes and commit them:
       ```bash
       git commit -m "Add a meaningful commit message"
       ```
    4. Push to your branch and submit a pull request.

    ---

    ## License
    This project is licensed under the HIT License.

    ---

    ## Notes for Professors and Reviewers
    - **Portability**: The application uses Docker and Docker Compose to simplify setup. Ensure Docker is installed on your machine.
    - **Customization**: Modify the `.env` file for any specific database or security configurations.
    - **Running Locally**: Use the provided `docker-compose.yml` file for seamless integration of the FastAPI backend and PostgreSQL.
    """
