class README:
    content = """
    # Pawfect Planner 🐾  
    **A backend application for managing pet profiles, reminders, vaccinations, and more. Built with FastAPI.**

    ---

    ## Features
    - **Pet Profiles**: Create and manage detailed profiles for your pets.
    - **Vaccination Tracking**: Check and track pet vaccinations.
    - **Reminders**: Set and manage reminders for vet visits, vaccinations, or other events.
    - **Health Check**: Basic health status API for monitoring.
    - **ICS Calendar Export**: Export reminders to `.ics` calendar files.
    - **Dynamic Breed Information**: Fetch breed-related information dynamically using APIs.
    - **Dockerized**: Fully containerized backend for ease of deployment.

    ---

    ## Prerequisites
    - Install **Docker** and **Docker Compose** on your system:
      - [Get Docker](https://docs.docker.com/get-docker/)
      - [Install Docker Compose](https://docs.docker.com/compose/install/)

    ---

    ## Installation and Setup

    ### Clone the Repository
    ```bash
    git clone https://github.com/EASS-HIT-PART-A-2024-CLASS-VI/PawfectPlanner.git
    cd PawfectPlanner
    ```

    ### Using Docker Compose
    1. Build and run the application:
       ```bash
       docker-compose up --build
       ```

    2. Open your browser and navigate to:
       ```
       http://localhost:8000
       ```

    3. **Swagger API Docs** (Interactive API):
       ```
       http://localhost:8000/docs
       ```

    4. **ReDoc API Docs**:
       ```
       http://localhost:8000/redoc
       ```

    ---

    ## Docker Compose Details

    ### Services
    - `app`: The FastAPI backend.
    - `db`: PostgreSQL database for storing pet profiles, reminders, and other information.

    ### Ports
    - FastAPI backend: **8000**
    - PostgreSQL database: **5432**

    ---

    ## Environment Variables
    Create a `.env` file in the root directory with the following content:

    ```plaintext
    DATABASE_URL=postgresql://postgres:password@db:5432/pawfectplanner
    SECRET_KEY=your-secret-key
    ACCESS_TOKEN_EXPIRE_MINUTES=60
    ```

    Replace `your-secret-key` with a secure key.

    ---

    ## Project Structure

    ```plaintext
    PawfectPlanner/
    ├── app/
    │   ├── routes/
    │   │   ├── breeds.py
    │   │   ├── healthcheck.py
    │   │   ├── pets.py
    │   │   ├── reminders.py
    │   │   ├── treatments.py
    │   │   └── vet_search.py
    │   ├── vaccines/
    │   │   ├── cat_vaccines.json
    │   │   ├── dog_vaccines.json
    │   │   └── vaccines.py
    │   ├── auth.py
    │   ├── database.py
    │   ├── main.py
    │   ├── models.py
    │   ├── schemas.py
    │   ├── security.py
    │   └── util.py
    ├── docker-compose.yml
    ├── Dockerfile
    ├── requirements.txt
    └── README.md
    ```

    ---

    ## Running Tests
    1. Run tests locally using `pytest`:
       ```bash
       pytest
       ```

    2. Inside the Docker container:
       ```bash
       docker exec -it pawfect-planner_app_1 pytest
       ```

    ---

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
