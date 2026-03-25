# Complete CI/CD & DevOps Reference Guide

This document is your master cheat sheet for managing this project, understanding its architecture, and building brand new projects from scratch using Docker, GitHub Actions, and AWS.

---

## 1. Core Architecture: Dev / Stage / Prod
Managing different environments is critical to releasing stable code without breaking the live website.

*   **Development (`dev`):** Your local laptop. You write code, test it instantly using `docker compose up` (which supports hot-reloading), and connect to a local dummy database.
*   **Staging/QA (`staging`):** A pre-production cloud environment. Before code goes to the real users, you merge it into staging. The CI/CD pipeline tests it and deploys it to a separate, private AWS server so your QA team can try to break it.
*   **Production (`main` / `prod`):** The live internet. Only perfectly tested, reviewed code from `staging` is merged here. The CI/CD pipeline deploys this directly to your live AWS EC2 and RDS instances.

---

## 2. Docker Fundamentals

Docker allows your application to run perfectly on *any* computer, regardless of its operating system or installed software.

*   **Dockerfile:** This is the text "Blueprint". It tells Docker exactly what OS to use (Ubuntu/Linux), what software to install (Python 3.11), and where to copy your code.
*   **Docker Image:** The packaged, executable outcome of the Blueprint. Think of it like a `.exe` or a `.zip` file that contains your entire application and its dependencies.
*   **Docker Container:** A running instance of an Image. You can run 5 identical containers (instances) from 1 Image.
*   **Docker Compose (`docker-compose.yml`):** A tool for defining and running multi-container Docker applications (e.g., your FastAPI app *and* a local MySQL database). It is primarily used to make local development 1-click easy instead of typing out massive `docker run` commands.

---

## 3. GitHub Actions (`.github/workflows/ci.yml`)

The `ci.yml` file is the brain of your Automation Robot. It contains 4 distinct Phases:

1.  **Phase 1: Download & Setup:** The robot wakes up in the cloud, installs Python, and downloads your latest code.
2.  **Phase 2: Automated Testing (`test_main.py`):** The robot runs `pytest`. If any of your code breaks the tests, the robot turns **RED** and completely halts the deployment to protect the live server.
3.  **Phase 3: Docker Build & Push:** If tests pass, the robot builds a brand new Docker Image based on your updated code and uploads (pushes) it to Docker Hub, so the rest of the world can download it.
4.  **Phase 4: SSH Deployment (AWS):** The robot securely logs into your blank AWS EC2 server, stops the old code, downloads the brand new Image from Docker Hub, and spins it up. 

---

## 4. AWS Configuration Details

*   **EC2 (Elastic Compute Cloud):** A raw, naked Linux computer you rent by the hour. We installed Docker on it and told it to leave Port 80 open so the public internet can request data from it.
*   **RDS (Relational Database Service):** A fully managed database. Instead of installing MySQL yourself on the EC2, AWS manages backups, scaling, and security. We configured the "Security Groups" so that *only* your specific EC2 server is allowed to talk to the RDS database.
*   **GitHub Secrets:** How the robot accesses AWS. Passwords like `EC2_SSH_KEY` (your `.pem` file) and `PROD_DB_PASSWORD` are safely stored in GitHub. They are injected into the robot's script so your passwords are never saved in your public code repository.

---

## 5. Command Cheat Sheet

### 🔹 Git & GitHub Commands
*   `git status` : Check which files you have modified.
*   `git add .` : Stage ALL modified files to be saved.
*   `git commit -m "added login page"` : Save the snapshot with a descriptive message.
*   `git push origin dev` : Upload your saved code to the `dev` branch on GitHub (Triggers CI/CD!).
*   `git checkout -b new-feature` : Create a brand new branch called *new-feature* and switch to it.
*   `git pull` : Download the newest code from GitHub to your laptop.

### 🔹 Docker Local Development
*   `docker build -t fastapi-app .` : Manually build an Image using the `Dockerfile` in the current folder.
*   `docker run --env-file .env -p 8000:8000 fastapi-app` : Manually run an Image and expose it to your browser on Port 8000.
*   `docker compose up` : Start your entire application locally using the `docker-compose.yml` file (Supports Hot-Reloading!).
*   `docker compose down` : Stop and delete the running local containers.

### 🔹 Python Testing
*   `pip install pytest httpx` : Install the required testing frameworks.
*   `python -m pytest` : Automatically find and run all tests in the `tests/` folder and show green passes or red fails.

---

## 6. How to Start a Brand New Project (End-to-End Checklist)

Whenever you want to build a completely new API from absolute scratch, follow these exact steps:

### Step 1: Write the Core Code
1. Write your Python API (`main.py`).
2. Write at least one automated test (`tests/test_main.py`).
3. Ensure all Python packages are saved inside a `requirements.txt` file.

### Step 2: Dockerize It
1. Create a `Dockerfile` that packages your code into a Linux environment.
2. Create a `docker-compose.yml` for local 1-click hot-reloading.
3. Add a `.dockerignore` and `.gitignore` so you don't accidentally package or upload your `.env` passwords!

### Step 3: Setup GitHub Automation
1. Create an empty repository on GitHub and push your code to a `dev` branch.
2. Go to GitHub Settings -> Secrets -> Actions. 
3. Add your Docker Hub credentials (`DOCKER_USERNAME` and `DOCKER_PASSWORD` using a Personal Access Token).
4. Create `.github/workflows/ci.yml` in your project folder, and program it to run tests and push the image to Docker Hub.

### Step 4: Provision Cloud Infrastructure (AWS)
1. Launch an Ubuntu EC2 Instance (Save the `.pem` key!).
2. Launch a MySQL RDS Database (Connect it directly to your EC2 instance's Security Group).
3. Copy the EC2 Public IP, the `.pem` text, and the RDS Endpoint URL.

### Step 5: Finalize the Pipeline
1. Add the AWS secrets to GitHub (`EC2_HOST`, `EC2_USERNAME`, `EC2_SSH_KEY`, `PROD_DB_HOST`, `PROD_DB_PASSWORD`, `PROD_DB_USER`).
2. Update the bottom of your `ci.yml` file to SSH into the EC2 Server, pull the Docker Image, and run it injected with the Production Database passwords.
3. Push the `ci.yml` file to GitHub and watch your pipeline deploy your new site live to the world!
