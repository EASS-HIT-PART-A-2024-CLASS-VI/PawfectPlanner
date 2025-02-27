🐾 Pawfect Planner

![Happy Pet](frontend/public/EntryBackground.png)

<div align="center">
  ![Pawfect Planner](https://raw.githubusercontent.com/EASS-HIT-PART-A-2024-CLASS-VI/PawfectPlanner/main/frontend/public/EntryBackground.png)

  **A microservices-based pet management solution powered by AI and modular architecture.**

  [![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
  [![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org)
  [![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
  [![Gemini AI](https://img.shields.io/badge/Gemini-AI-blue?style=for-the-badge&logo=google&logoColor=white)](https://gemini.google.com/chat)
  [![The Dog API](https://img.shields.io/badge/The%20Dog%20API-🐶-blue?style=for-the-badge)](https://thedogapi.com/)
</div>

🎥 Demo
📽️ Coming soon!

📌 Features
🔹 Backend
✅ Pet Profiles 🐶🐱 – Manage detailed pet profiles, including breed, age, weight, behavior issues, and health history.
✅ Vaccination Tracking 💉 – Store vaccination records and upcoming vaccinations.
✅ Reminders ⏰ – Set and manage reminders for vet visits, vaccinations, and medications.
✅ ICS Calendar Export 📅 – Export reminders to .ics files for Google Calendar, Outlook, etc.
✅ Dynamic Breed Information 🔍 – Fetch breed-related data from external APIs (The Dog API, The Cat API).
✅ Local Vet Search 🏥 – Locate nearby veterinary clinics using Google Maps.
✅ Secure Authentication 🔐 – Implements JWT authentication and user authorization.
✅ Microservices Architecture 🏗️ – Modular services (LLM [Google Gemini], PDF export of pet profiles, ICS reminders).
🔹 Frontend
✅ React-based UI 🎨 – A clean, user-friendly interface for pet data management.
✅ Interactive Reminders & Notifications 🔔 – Auto-renewing reminders (ICS files) to prevent missing treatments.

🛠️ Technologies Used
Backend

🚀 FastAPI (Python 3.12) – High-performance API framework.
🗄 PostgreSQL – Relational database for secure pet data storage.
📡 SQLAlchemy – ORM for database interactions.
🔑 JWT Authentication – Secure user authentication.
📅 ICS Library – Export reminders as .ics calendar files.
📄 Data to PDF Service – Convert pet data into downloadable PDFs.
🐶 The Dog API & The Cat API – Fetch breed-related health and behavior data.
🤖 LLM - Gemini AI – Provides pet advice and fills missing API data.
🐳 Docker & Docker Compose – Fully containerized for easy deployment.

Frontend

⚡ React + Vite – Fast UI framework for single-page applications.
🏛 React Router – Enables navigation between pages.
🎛 Redux/Zustand – Manages application state efficiently.
🎨 Styled Components / Tailwind CSS – Modern styling techniques.
🔄 Axios – Handles API requests seamlessly.


⚙️ Prerequisites
Ensure you have:
✅ Docker installed.
✅ Docker Compose installed.
✅ Python 3.12 (for local development).

🚀 Installation and Setup
1️⃣ Clone the Repository
'''git clone https://github.com/EASS-HIT-PART-A-2024-CLASS-VI/PawfectPlanner.git
cd PawfectPlanner'''

2️⃣ Set Up Environment Variables
Create a .env file at the root directory:
'''echo 'POSTGRES_USER=postgres
POSTGRES_PASSWORD=DB4PawfectPlanner
POSTGRES_DB=pets_db
DATABASE_URL=postgresql://postgres:DB4PawfectPlanner@db:5432/pets_db
GEMINI_API_KEY=<YOUR_GEMINI_API_KEY>
DOG_API_KEY=<YOUR_DOG_API_KEY>' > .env'''

💡 Note: Replace <YOUR_GEMINI_API_KEY> and <YOUR_DOG_API_KEY> with valid API keys. All PostgreSQL data is public, feel free to use it or replace with your own.
Need an API key? follow links and instructions here <https://ai.google.dev/gemini-api/docs/api-key> for Gemini API KEY, and here <https://www.thedogapi.com/> for The Dog API key (works for The Cat API as well)

🐳 Running the Project with Docker
3️⃣ Start the Full Application
Run Docker Compose to build and launch all services (backend, frontend, database, and microservices):
'''docker compose up --build'''

4️⃣ Access the Services:

🚀 FastAPI Backend → http://localhost:8000
📑 API Docs (Swagger UI) → http://localhost:8000/docs
🎨 Frontend UI (React) → http://localhost:3000 (or next available port if 3000 is taken)


🗄️ Project Structure
PawfectPlanner/
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── breeds.py
│   │   │   ├── healthcheck.py
│   │   │   ├── ics_generator.py
│   │   │   ├── pets.py
│   │   │   ├── reminders.py
│   │   │   ├── treatments.py
│   │   │   ├── vet_search.py
│   │   ├── vaccines/
│   │   │   ├── cat_vaccines.json
│   │   │   ├── dog_vaccines.json
│   │   │   ├── vaccines.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── security.py
│   │   ├── util.py
│   ├── gemini-service/
│   │   ├── Dockerfile
│   │   ├── app.py
│   │   ├── gemini_api_helper.py
│   │   ├── query_gemini.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── README.md
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── styles/
│   │   ├── utils/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   ├── Dockerfile
│   ├── package.json
├── docker-compose.yml
└── README.md

✅ Running Tests
Run Locally:
pytest

Run Inside Docker:
'''docker exec -it pawfect-planner_app_1 pytest'''

🆘 Troubleshooting
1️⃣ Reset & Rebuild Everything
'''docker compose down --rmi all --volumes --remove-orphans
docker compose up --build'''

2️⃣ Reset Frontend
'''cd frontend
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
npm run dev'''

3️⃣ Reset Backend (Python Virtual Environment)
'''cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload'''


🎉 Get Started with Pawfect Planner!
🚀 Ready to manage your pet’s care effortlessly?
📢 Join Pawfect Planner today and make pet management hassle-free! 🐾
📧 Contact: barnir16@gmail.com
