"""
CodeCraftHub - A Simple Personalized Learning Platform
======================================================

This Flask application provides a REST API for developers to track
courses they want to learn. Course data is stored in a simple JSON
file (no database required).

Endpoints:
    POST   /api/courses        - Add a new course
    GET    /api/courses        - Get all courses
    GET    /api/courses/<id>   - Get a specific course
    PUT    /api/courses/<id>   - Update a course
    DELETE /api/courses/<id>   - Delete a course
"""

# ──────────────────────────────────────────────
# 1. IMPORTS
# ──────────────────────────────────────────────
# Flask      → the web framework that handles HTTP requests
# jsonify    → converts Python dicts/lists into JSON responses
# request    → gives access to incoming request data (body, params)
import json               # read/write JSON files
import os                 # check if files exist on disk
from datetime import datetime  # generate timestamps

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

# ──────────────────────────────────────────────
# 2. APP CONFIGURATION
# ──────────────────────────────────────────────
app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# Path to our "database" — a simple JSON file in the same directory
COURSES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "courses.json")

# The only status values we allow for a course
VALID_STATUSES = ["Not Started", "In Progress", "Completed"]


# ──────────────────────────────────────────────
# 3. JSON FILE HELPER FUNCTIONS
# ──────────────────────────────────────────────
# These two functions handle ALL file I/O.
# Every route uses them instead of touching the file directly.

def load_courses():
    """
    Read courses from the JSON file and return them as a Python list.

    If the file doesn't exist yet (first run), return an empty list.
    This means the app creates courses.json automatically on the
    first POST request.
    """
    # If the file doesn't exist, start fresh
    if not os.path.exists(COURSES_FILE):
        return []

    try:
        with open(COURSES_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            # Ensure we always return a list, even if the file is malformed
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError) as error:
        # If the file is corrupted or unreadable, log and return empty
        print(f"⚠️  Error reading {COURSES_FILE}: {error}")
        return []


def save_courses(courses):
    """
    Write the full list of courses to the JSON file.

    Uses indent=2 for pretty-printing so the file is easy to
    inspect manually — great for learning and debugging!
    """
    try:
        with open(COURSES_FILE, "w", encoding="utf-8") as file:
            json.dump(courses, file, indent=2, ensure_ascii=False)
        return True
    except IOError as error:
        print(f"⚠️  Error writing to {COURSES_FILE}: {error}")
        return False


def get_next_id(courses):
    """
    Generate the next course ID.

    Strategy: find the highest existing ID and add 1.
    If the list is empty, start at 1.

    Example:
        courses = [{"id": 1}, {"id": 3}]  →  returns 4
        courses = []                        →  returns 1
    """
    if not courses:
        return 1
    return max(course["id"] for course in courses) + 1


# ──────────────────────────────────────────────
# 4. INPUT VALIDATION HELPER
# ──────────────────────────────────────────────

def validate_course_data(data, is_update=False):
    """
    Validate incoming course data from a POST or PUT request.

    For POST (is_update=False):
        All fields are required: name, description, target_date, status.

    For PUT (is_update=True):
        Only validate fields that are actually provided.
        This allows partial updates (e.g. update just the status).

    Returns:
        (None, None)          if validation passes
        (error_message, 400)  if validation fails
    """
    # --- Check required fields on creation ---
    if not is_update:
        required_fields = ["name", "description", "target_date", "status"]
        for field in required_fields:
            if field not in data or not str(data[field]).strip():
                return (
                    jsonify({"error": f"'{field}' is required and cannot be empty"}),
                    400,
                )

    # --- Validate 'name' if provided ---
    if "name" in data and not str(data["name"]).strip():
        return jsonify({"error": "Course name cannot be empty"}), 400

    # --- Validate 'status' if provided ---
    if "status" in data and data["status"] not in VALID_STATUSES:
        return (
            jsonify({
                "error": f"Invalid status '{data['status']}'. "
                         f"Must be one of: {', '.join(VALID_STATUSES)}"
            }),
            400,
        )

    # --- Validate 'target_date' format if provided ---
    if "target_date" in data:
        try:
            datetime.strptime(data["target_date"], "%Y-%m-%d")
        except ValueError:
            return (
                jsonify({"error": "Invalid date format. Use YYYY-MM-DD (e.g. 2026-05-15)"}),
                400,
            )

    # All checks passed
    return None, None


# ──────────────────────────────────────────────
# 5. API ROUTES
# ──────────────────────────────────────────────

# ---- Home / Welcome (Now serves the Dashboard) ----
@app.route("/")
def home():
    """
    Serves the dashboard HTML file.
    """
    return send_file("index.html")


# ──────────────────────────
# CREATE — POST /api/courses
# ──────────────────────────
@app.route("/api/courses", methods=["POST"])
def create_course():
    """
    Add a new course to the learning tracker.

    Expects a JSON body with:
        - name         (string, required)
        - description  (string, required)
        - target_date  (string, required, format YYYY-MM-DD)
        - status       (string, required, one of VALID_STATUSES)

    The server auto-generates:
        - id           (integer, auto-incremented)
        - created_at   (ISO 8601 timestamp)
    """
    # Step 1: Make sure the request contains JSON
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    # Step 2: Validate the input
    error, status_code = validate_course_data(data)
    if error:
        return error, status_code

    # Step 3: Load existing courses
    courses = load_courses()

    # Step 4: Build the new course object
    new_course = {
        "id": get_next_id(courses),
        "name": data["name"].strip(),
        "description": data["description"].strip(),
        "target_date": data["target_date"],
        "status": data["status"],
        "created_at": datetime.now().isoformat(),
    }

    # Step 5: Append and save
    courses.append(new_course)

    if not save_courses(courses):
        return jsonify({"error": "Failed to save course. Please try again."}), 500

    # Step 6: Return the created course with 201 Created
    return jsonify({
        "message": "Course created successfully",
        "course": new_course,
    }), 201


# ────────────────────────────
# READ ALL — GET /api/courses
# ────────────────────────────
@app.route("/api/courses", methods=["GET"])
def get_all_courses():
    """
    Retrieve all courses from the tracker.

    Returns a JSON object with:
        - count   (int)  — total number of courses
        - courses (list) — array of course objects
    """
    courses = load_courses()
    return jsonify({
        "count": len(courses),
        "courses": courses,
    }), 200


# ──────────────────────────────────
# READ ONE — GET /api/courses/<id>
# ──────────────────────────────────
@app.route("/api/courses/<int:course_id>", methods=["GET"])
def get_course(course_id):
    """
    Retrieve a single course by its ID.

    URL parameter:
        course_id (int) — the unique ID of the course

    Returns 404 if no course with that ID exists.
    """
    courses = load_courses()

    # Search for the course with the matching ID
    course = next(
        (c for c in courses if c["id"] == course_id),
        None,  # default if not found
    )

    if course is None:
        return jsonify({"error": f"Course with id {course_id} not found"}), 404

    return jsonify({"course": course}), 200


# ──────────────────────────────────
# UPDATE — PUT /api/courses/<id>
# ──────────────────────────────────
@app.route("/api/courses/<int:course_id>", methods=["PUT"])
def update_course(course_id):
    """
    Update an existing course.

    Supports partial updates — you only need to send the fields
    you want to change. For example, to mark a course as completed:

        PUT /api/courses/1
        {"status": "Completed"}

    Updatable fields: name, description, target_date, status
    The id and created_at fields cannot be changed.
    """
    # Step 1: Parse JSON body
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    # Step 2: Validate (partial mode)
    error, status_code = validate_course_data(data, is_update=True)
    if error:
        return error, status_code

    # Step 3: Load and find the course
    courses = load_courses()
    course = next(
        (c for c in courses if c["id"] == course_id),
        None,
    )

    if course is None:
        return jsonify({"error": f"Course with id {course_id} not found"}), 404

    # Step 4: Update only the fields that were provided
    updatable_fields = ["name", "description", "target_date", "status"]
    for field in updatable_fields:
        if field in data:
            value = data[field].strip() if isinstance(data[field], str) else data[field]
            course[field] = value

    # Step 5: Save
    if not save_courses(courses):
        return jsonify({"error": "Failed to save changes. Please try again."}), 500

    return jsonify({
        "message": "Course updated successfully",
        "course": course,
    }), 200


# ──────────────────────────────────────
# DELETE — DELETE /api/courses/<id>
# ──────────────────────────────────────
@app.route("/api/courses/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    """
    Delete a course by its ID.

    Returns the deleted course object for confirmation.
    Returns 404 if no course with that ID exists.
    """
    courses = load_courses()

    # Find the course
    course = next(
        (c for c in courses if c["id"] == course_id),
        None,
    )

    if course is None:
        return jsonify({"error": f"Course with id {course_id} not found"}), 404

    # Remove it from the list
    courses = [c for c in courses if c["id"] != course_id]

    # Save the updated list
    if not save_courses(courses):
        return jsonify({"error": "Failed to save changes. Please try again."}), 500

    return jsonify({
        "message": "Course deleted successfully",
        "deleted_course": course,
    }), 200


# ──────────────────────────────────────────────
# 6. RUN THE APPLICATION
# ──────────────────────────────────────────────
if __name__ == "__main__":
    # debug=True enables:
    #   - Auto-reload when you save code changes
    #   - Detailed error pages in the browser
    # ⚠️  Never use debug=True in production!
    print("=" * 50)
    print("🚀 CodeCraftHub API is starting...")
    print(f"📂 Courses file: {COURSES_FILE}")
    print("📡 Server: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True)
