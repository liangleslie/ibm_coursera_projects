# 🚀 CodeCraftHub

A simple, personalized learning platform for developers to track courses they want to learn. Built for beginners to learn REST API basics using **Python Flask** and a **JSON file** for storage.

---

## 📖 Project Overview
CodeCraftHub is a lightweight backend application that acts as your personal learning assistant. Instead of using a complex database, it stores your progress in a simple text file (`courses.json`). It provides a standard REST API that can be used by any frontend or testing tool (like `curl` or Postman).

---

## ✨ Features
- **Full CRUD Operations**: Create, Read, Update, and Delete courses.
- **Persistent Storage**: Your data stays safe in a JSON file even if the server restarts.
- **Auto-ID Generation**: New courses automatically get a unique ID.
- **Input Validation**: Ensures you don't save empty names or invalid status values.
- **Automatic Setup**: Creates the data file automatically on the first update.

---

## 📂 Project Structure Explained
```text
├── app.py            # The heart of the app. Contains the server logic and API routes.
├── courses.json      # Your local "database". A human-readable text file.
├── requirements.txt  # A list of Python libraries needed (Flask).
├── test_api.py       # An automated script to verify everything is working.
└── README.md         # This guide!
```

---

## 🛠️ Installation (Step-by-Step)

### 1. Prerequisite
Ensure you have **Python 3.7+** installed. You can check by running:
```bash
python --version
```

### 2. Set up a Virtual Environment (Recommended)
This keeps the project dependencies isolated.
```bash
python -m venv my_env
source my_env/bin/activate  # On Windows: my_env\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run the Application

Start the Flask development server:
```bash
python app.py
```
You should see output indicating the server is running at `http://127.0.0.1:5000`.

---

## 📡 API Documentation & Test Cases

Below are the `curl` commands to test every feature. These are perfect for copy-pasting into your terminal!

### 1. List All Courses
**Request:**
```bash
curl http://127.0.0.1:5000/api/courses
```
**Expected Response (200 OK):**
```json
{
  "count": 3,
  "courses": [...]
}
```

### 2. Add a New Course
**Request:**
```bash
curl -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Advanced Python",
    "description": "Deep dive into decorators and generators",
    "target_date": "2026-12-01",
    "status": "Not Started"
  }'
```
**Expected Response (201 Created):**
```json
{
  "course": { "id": 4, "name": "Advanced Python", ... },
  "message": "Course created successfully"
}
```

### 3. Get a Specific Course
**Request:**
```bash
curl http://127.0.0.1:5000/api/courses/4
```
**Expected Response (200 OK):**
```json
{
  "course": { "id": 4, "name": "Advanced Python", ... }
}
```

### 4. Update Course Status
**Request:**
```bash
curl -X PUT http://127.0.0.1:5000/api/courses/4 \
  -H "Content-Type: application/json" \
  -d '{"status": "In Progress"}'
```
**Expected Response (200 OK):**
```json
{
  "course": { "status": "In Progress", ... },
  "message": "Course updated successfully"
}
```

### 5. Delete a Course
**Request:**
```bash
curl -X DELETE http://127.0.0.1:5000/api/courses/4
```
**Expected Response (200 OK):**
```json
{ "message": "Course deleted successfully", "deleted_course": { ... } }
```

---

## ⚠️ Error Scenario Test Cases

### Test: Missing Required Fields
**Request:**
```bash
curl -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{"name": "Incomplete"}'
```
**Expected Response (400 Bad Request):**
```json
{ "error": "'description' is required and cannot be empty" }
```

### Test: Invalid Status Value
**Request:**
```bash
curl -X PUT http://127.0.0.1:5000/api/courses/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "Loving It"}'
```
**Expected Response (400 Bad Request):**
```json
{ "error": "Invalid status 'Loving It'. Must be one of: Not Started, In Progress, Completed" }
```

### Test: Course Not Found
**Request:**
```bash
curl http://127.0.0.1:5000/api/courses/999
```
**Expected Response (404 Not Found):**
```json
{ "error": "Course with id 999 not found" }
```

---

## 🧪 Automated Testing
If you prefer not to use `curl`, you can use the built-in test script:
```bash
python test_api.py
```

---

## 🔍 Troubleshooting

| Issue | Solution |
|-------|----------|
| **"Address already in use"** | Another app is using port 5000. Close it or use `app.run(port=5001)` in `app.py`. |
| **"ModuleNotFoundError: No module named 'flask'"** | Ensure you have activated your virtual environment and run `pip install -r requirements.txt`. |
| **JSON file errors** | Check if `courses.json` has valid JSON syntax. If it's corrupted, you can safely delete it and the app will create a new one. |
| **Changes not reflecting** | Flask debug mode should auto-restart the server, but you can try manually stopping (`Ctrl+C`) and starting it again. |

---

## 📝 Learning Concepts
- **HTTP Methods**: GET (read), POST (create), PUT (update), DELETE (remove).
- **Status Codes**: 200 (Success), 201 (Created), 400 (Client Error), 404 (Not Found).
- **JSON Serialization**: Converting Python objects to text-based JSON and back.
