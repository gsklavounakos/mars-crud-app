*This repository is made for educational purposes.

It is made according to the tasks of the of the first Lab homework for the university subject - Software Engineering In Practice- at Athens University of Economics and Business, Department of Management Science and Technology. The project's description is:

🚀 Mission: Mars Deployment - CI/CD Challenge 🌌

Mission Briefing

Congratulations, engineer! You have been selected as the Lead DevOps Engineer for SpaceX MarsOps, a team responsible for deploying the first-ever Martian CRUD (Create, Read, Update, Delete) Application. Your task is to set up a fully automated CI/CD pipeline that ensures our Mission Control CRUD System (a simple CRUD app) is always built, tested, and packaged properly.

However, the mission has strict compliance, reliability, and automation requirements! You must ensure:

1. Code is always tested before packaging
2. Builds are automated and optimized

🛠️ Mission Tasks

🚦 Phase 1: Mission Repository Initialization

Create a Git repository for your project (GitHub).
Create and add a simple CRUD application that manages space station resource stock (e.g., product name, id, quantity ) using a relational or NoSQL database (preferably in-memory) and exposes the required REST endpoints.
Supported stacks: Flask/Django, Node.js (Express), Java (Spring Boot), DBs: SQLite, H2, MongoDB etc.
Ensure the application runs locally and document the setup in a README.md.
Push the code to your repository.

🚀 Phase 2: CI - Mission Safety Checks
Goal: Ensure the mission code is always tested and reviewed before proceeding to the next phase.

Choose a CI/CD tool (GitHub Actions).
Implement automated checks:
Code Quality Check using ESLint/PyLint/Checkstyle.
Unit Tests with Jest, PyTest, or JUnit.
Configure branch protection rules:
Only merge changes into the main branch after passing checks.
Mission Success Criteria:
Every code commit triggers a CI pipeline that performs tests and quality checks.

🚢 Phase 3: Build Automation - The Martian Compiler
Goal: Automate the application build process to ensure a deployable artifact.

Use a build automation tool:
Java → Use Maven/Gradle to generate a .jar file.
Python → Use setup.py and package the app.
Node.js → Use webpack or npm build.
Dockerize the application:
Write a Dockerfile to package the app.
Build the Docker image and store it in Docker Hub (ensure the confidentiality of your docker credentials by storing them as GitHub secrets).
Mission Success Criteria:
The CI pipeline automatically builds and stores a deployable artifact.

🎯 Bonus Challenge: Intergalactic Infrastructure as Code (IaC) + Simple UI
(Optional, for extra credit!)

Use Docker Compose to automate local environment setup.
Create a very simple UI (JavaScript-based, using React, Vue, or plain HTML/CSS/JS) to interact with the CRUD application.
Docker Compose the frontend with the backend (CRUD App), ensuring they run together seamlessly.
🛠️ Mission Tasks' Documentation
Mission 1
Developer Setup Guide

To set up the project locally, follow these steps:

1. Clone the repository:
    
    git clone https://github.com/gsklavounakos/mars-crud-app.git
    
2. Navigate to the project directory:
    
    cd mars-crud-app
   
3. Install the required dependencies:

    pip install -r requirements.txt


4. Create the database:

    python db.py



5. Run the application:

    python app.py

6. Access the API at `http://127.0.0.1:5000/resources` in your browser or API tool (Postman, cURL, etc.).

**Note:** Make sure one of the latest Python releases is installed on your system.
