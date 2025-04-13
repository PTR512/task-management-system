# 📌 Task Management System

A lightweight RESTful API for managing projects and tasks. Built with **Flask** and **PostgreSQL**, this backend service enables efficient tracking of projects and tasks, including filtering, due dates, and priorities. The app is fully containerized using Docker and tested with 90%+ coverage using **pytest**.

---

## 🚀 Features

- Project and task management with one-to-many relationship
- Task filtering by status, priority, and project
- RESTful API architecture
- Dockerized deployment with Docker Compose
- 90%+ test coverage using pytest
- Clean architecture (models, services, routes separation)

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Database:** PostgreSQL
- **Testing:** Pytest
- **Containerization:** Docker, Docker Compose
- **API style:** RESTful

---

## 📬 API Endpoints

### 🔹 Projects

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/api/projects` | Get all projects |
| GET    | `/api/projects/{id}` | Get project details |
| GET    | `/api/projects/{id}?include_tasks=true` | Get project with its tasks |
| GET    | `/api/projects/{id}/tasks` | Get all tasks in a project |
| POST   | `/api/projects` | Create a new project |
| PUT    | `/api/projects/{id}` | Update a project |
| DELETE | `/api/projects/{id}` | Delete a project and its tasks |

---

### 🔹 Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/api/tasks` | Get all tasks |
| GET    | `/api/tasks?status=todo&priority=high&project_id=1` | Filter tasks by query parameters |
| GET    | `/api/tasks/{id}` | Get task details |
| POST   | `/api/tasks` | Create a new task |
| PUT    | `/api/tasks/{id}` | Update a task |
| DELETE | `/api/tasks/{id}` | Delete a task |

---

## 🔧 Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/task-management-system.git
cd task-management-system
```

2. Install required dependencies
```bash
pip install -r requirements.txt
```

3. Run with Docker
```bash
docker-compose up --build
```
The API will be available at: http://localhost:5000/api/

---

## 📄 License
[MIT License](LICENSE)
