# 🐾 Pawfect Planner

<div align="center">
  <img src="frontend/public/EntryBackground.png" alt="Pawfect Planner Logo" width="50%">

  [![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
  [![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org)
  [![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
  [![Gemini AI](https://img.shields.io/badge/Gemini-AI-blue?style=for-the-badge&logo=google&logoColor=white)](https://gemini.google.com/chat)
  [![The Dog API](https://img.shields.io/badge/The%20Dog%20API-🐶-blue?style=for-the-badge)](https://thedogapi.com/)

  **A microservices-based pet management solution powered by AI and modular architecture.**
</div>

---

## 🎥 Demo
<a href="https://youtu.be/evx-q7IXau8" target="_blank">
  <img  
    alt="PawfectPlanner demo" 
    width="100%"
  />
</a>

---

## 📌 Features

### 🔹 Backend
- **Pet Profiles** (dog/cat/other) – Manage pet info (breed, age, weight, health & behavior issues).
- **Reminders** – Create events (vet visits, medications, etc.) with ICS export for calendar apps.
- **Vaccination Tracking** – Store upcoming vaccinations and show next due dates.
- **Breed Information** – Pull breed-specific data (life expectancy, recommended weight, etc.) from [The Dog API](https://thedogapi.com/) & [The Cat API](https://thecatapi.com/).
- **PDF Exports** – Generate PDF summaries for pet profiles.
- **AI Chat** – Connect to Google’s Gemini LLM for pet advice & suggestions.
- **JWT Auth** – Secure user authentication with token-based login.
- **Microservices** – Separate containers for the main backend, LLM service, database, and caching (Redis).

### 🔹 Frontend
- **React-based UI** – Modern single-page application for creating/managing pets & reminders.
- **Nginx Container** – Serves the built React app and can proxy requests to the backend.
- **Reminders & Notifications** – Easy to set repeated tasks with ICS downloads (“Add to Calendar”).
- **Gemini Chat** – Ask pet care questions with optional automatic injection of your pet's data.

---

## 🛠️ Technologies Used

### Backend
- **FastAPI (Python 3.12)** – High-performance API framework.
- **PostgreSQL** – Relational DB for pet & user data.
- **SQLAlchemy** – ORM for schema & queries.
- **JWT Auth** – Secure token-based login.
- **ICalendar / ICS** – Exports reminders to `.ics` (Calendar).
- **PDF Generation** – Exports pet profiles to PDF.
- **The Dog API & The Cat API** – External breed data.
- **Redis** – Caching breed lookups & repeated calls.
- **Google Gemini** – AI-based pet advice & suggestions.
- **Docker Compose** – Container orchestration.

### Frontend
- **React + Vite** – Fast dev & build tool for React.
- **Nginx** – Container serving the production React build.
- **React Router** – Single-page routing.
- **Axios** – HTTP client for requests.
- **CSS Modules / Plain CSS** – Custom styling approach.

---

## ⚙️ Prerequisites 
- **Docker** & **WSL (Ubuntu)** installed.  
- (Optional) **Python 3.12** if you want local dev outside containers (expanding upon the project). 

---

## 🚀 Installation & Setup  

*Step 1: Start docker*  
Make sure Docker Desktop (or Docker Engine) is running. Only then open your WSL shell.

*Step 2: Clone the Repository from Github*  
 **Clone the Repository**:  
 Copy this command in WSL:  
   ```bash
   git clone https://github.com/EASS-HIT-PART-A-2024-CLASS-VI/PawfectPlanner.git
   cd PawfectPlanner
  ```

*Step 3: Create the .env File:*

Inside your WSL shell:

  ```bash
  cat <<EOF > .env
  POSTGRES_USER=postgres
  POSTGRES_PASSWORD=DB4PawfectPlanner
  POSTGRES_DB=pawfectplanner
  DATABASE_URL=postgresql://postgres:DB4PawfectPlanner@db:5432/pawfectplanner

  # External API keys
  GEMINI_API_KEY=<YOUR_GEMINI_API_KEY>
  DOG_API_KEY=<YOUR_DOG_API_KEY>

  DEBUG=true
  EOF
  ```

*Replace <YOUR_GEMINI_API_KEY> / <YOUR_DOG_API_KEY> with valid credentials.*

Need an API key?

 [Google Gemini API Key](https://ai.google.dev/gemini-api/docs/api-key)  

 [The Dog API key](https://www.thedogapi.com/) (works for The Cat API as well).  

 All PostgreSQL values are public, feel free to use them, or replace with your own (if you wish to create a separate DB, not recommended)  

*Step 4: Loading the project* 

Build & Launch with Docker: 

 ```bash 
 docker-compose build --no-cache  
 docker-compose up -d  
 ```

Services started: 

db (Postgres) on port 5432  
redis on port 6379  
backend (FastAPI) on port 8000  
gemini-service on port 5000 
frontend (Nginx + built React) on port 3000 

That's it! to access the App: 

Frontend: http://localhost:3000 
API Docs: http://localhost:8000/docs for Swagger. 
Gemini Chat: Access the “PawfectGPT” page from the main app UI (top nav). 


🗄️ Project Structure  

```plaintext
PawfectPlanner/
├── backend/
│   ├── gemini_service/
│   │   ├── Dockerfile
│   │   ├── __init__.py
│   │   └── geminiRun.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── breeds.py
│   │   ├── healthcheck.py
│   │   ├── ics_generator.py
│   │   ├── pets.py
│   │   ├── reminders.py
│   │   └── treatments.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── pytest.ini
│   │   ├── test_auth.py
│   │   ├── test_breed_info.py
│   │   ├── test_gemini.py
│   │   ├── test_pets.py
│   │   ├── test_reminders.py
│   │   └── test_validation.py
│   ├── vaccines/
│   │   ├── cat_vaccines.json
│   │   ├── dog_vaccines.json
│   │   └── vaccines.py
│   ├── Dockerfile
│   ├── __init__.py
│   ├── cache.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── requirements.txt
│   ├── schemas.py
│   ├── security.py
│   └── util.py
├── frontend/
│   ├── public/
│   │   ├── EntryBackground.png
│   │   ├── Project Diagram.drawio.png
│   │   ├── favicon.ico
│   │   └── vite.svg
│   ├── src/
│   │   ├── api/
│   │   │   └── geminiService.js
│   │   ├── assets/
│   │   │   └── react.svg
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   └── PrivateRoute.jsx
│   │   ├── context/
│   │   │   └── AuthContext.jsx
│   │   ├── pages/
│   │   │   ├── AddPet.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── EditPet.jsx
│   │   │   ├── Home.jsx
│   │   │   ├── Login.jsx
│   │   │   ├── PawfectGPT.jsx
│   │   │   ├── PetProfile.jsx
│   │   │   ├── Reminders.jsx
│   │   │   ├── ServiceLocator.jsx
│   │   │   ├── SignUp.jsx
│   │   │   └── Treatments.jsx
│   │   ├── routes/
│   │   │   └── routes.js
│   │   ├── services/
│   │   │   ├── authService.js
│   │   │   └── axiosSetup.js
│   │   ├── styles/
│   │   │   ├── AddPet.css
│   │   │   ├── App.css
│   │   │   ├── Auth.css
│   │   │   ├── Dashboard.css
│   │   │   ├── EditPet.css
│   │   │   ├── Home.css
│   │   │   ├── Navbar.css
│   │   │   ├── PawfectGPT.css
│   │   │   ├── PetProfile.css
│   │   │   ├── Reminders.css
│   │   │   ├── ServiceLocator.css
│   │   │   ├── Treatments.css
│   │   │   └── global.css
│   │   ├── utils/
│   │   │   └── generatePDF.js
│   │   ├── App.jsx
│   │   ├── config.js
│   │   └── main.jsx
│   ├── Dockerfile
│   ├── eslint.config.js
│   ├── index.html
│   ├── nginx.conf
│   ├── package-lock.json
│   ├── package.json
│   └── vite.config.js
├── README.md
├── docker-compose.yml
├── package-lock.json
└── package.json
```

✅ Running Tests  
Locally:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest
```

Inside Docker:
```bash
docker-compose exec backend pytest
```

🆘 Troubleshooting

running into issues?
Reset & Rebuild Everything:
```bash
docker-compose down --volumes --rmi all --remove-orphans
docker-compose build --no-cache
docker-compose up -d
```

backend seems to work but you're having issues loading frontend?
Reset Frontend:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
npm run dev
```

🎉 Get Started with PawfectPlanner! 
Ready to manage your pet’s care effortlessly and learn more about their needs?  
Join PawfectPlanner today and make pet management hassle-free! 🐾 
Contact: barnir16@gmail.com 

# *Future Features (Not Implemented in This Course)*

- Share pet information with other users (with seperation of read only/edit permissions)  
- Allow users to save pictures of their pets in pet profile, and add it to the PDF  
- Creation of a mobile version  
- Allow users to keep various details in a Timeline - easy storage of vet visit summaries for tracking, training progress, etc. 