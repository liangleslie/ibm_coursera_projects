"""
CodeCraftHub - API Test Script
==============================

Run this script WHILE the Flask server is running (in another terminal)
to test all API endpoints automatically.

Usage:
    1. Start the server:   python app.py
    2. Run the tests:      python test_api.py
"""

import requests

BASE_URL = "http://127.0.0.1:5000/api/courses"

# Formatting helpers
def header(text):
    print(f"\n{'=' * 60}")
    print(f"  {text}")
    print(f"{'=' * 60}")

def result(response):
    print(f"  Status: {response.status_code}")
    print(f"  Body:   {response.json()}")
    print()


# ──────────────────────────────────────────────
# Test 1: GET all courses (seed data)
# ──────────────────────────────────────────────
header("TEST 1: GET /api/courses — List all courses")
resp = requests.get(BASE_URL)
result(resp)

# ──────────────────────────────────────────────
# Test 2: POST — Create a new course
# ──────────────────────────────────────────────
header("TEST 2: POST /api/courses — Create a new course")
new_course = {
    "name": "Kubernetes Essentials",
    "description": "Learn container orchestration with K8s",
    "target_date": "2026-07-01",
    "status": "Not Started",
}
resp = requests.post(BASE_URL, json=new_course)
result(resp)
# Save the ID for later tests
created_id = resp.json().get("course", {}).get("id")

# ──────────────────────────────────────────────
# Test 3: GET — Retrieve the newly created course
# ──────────────────────────────────────────────
header(f"TEST 3: GET /api/courses/{created_id} — Get specific course")
resp = requests.get(f"{BASE_URL}/{created_id}")
result(resp)

# ──────────────────────────────────────────────
# Test 4: PUT — Update the course status
# ──────────────────────────────────────────────
header(f"TEST 4: PUT /api/courses/{created_id} — Update status to 'In Progress'")
resp = requests.put(f"{BASE_URL}/{created_id}", json={"status": "In Progress"})
result(resp)

# ──────────────────────────────────────────────
# Test 5: DELETE — Remove the course
# ──────────────────────────────────────────────
header(f"TEST 5: DELETE /api/courses/{created_id} — Delete course")
resp = requests.delete(f"{BASE_URL}/{created_id}")
result(resp)

# ──────────────────────────────────────────────
# Test 6: Error — GET a course that doesn't exist
# ──────────────────────────────────────────────
header("TEST 6: GET /api/courses/999 — Course not found (expect 404)")
resp = requests.get(f"{BASE_URL}/999")
result(resp)

# ──────────────────────────────────────────────
# Test 7: Error — POST with missing fields
# ──────────────────────────────────────────────
header("TEST 7: POST /api/courses — Missing required fields (expect 400)")
resp = requests.post(BASE_URL, json={"name": "Incomplete Course"})
result(resp)

# ──────────────────────────────────────────────
# Test 8: Error — POST with invalid status
# ──────────────────────────────────────────────
header("TEST 8: POST /api/courses — Invalid status value (expect 400)")
bad_course = {
    "name": "Bad Course",
    "description": "This has an invalid status",
    "target_date": "2026-08-01",
    "status": "Maybe",
}
resp = requests.post(BASE_URL, json=bad_course)
result(resp)

# ──────────────────────────────────────────────
# Final check: list all courses again
# ──────────────────────────────────────────────
header("FINAL: GET /api/courses — Verify final state")
resp = requests.get(BASE_URL)
data = resp.json()
print(f"  Total courses: {data['count']}")
for course in data["courses"]:
    print(f"    [{course['status']:12}] {course['name']}")
print()
print("✅ All tests completed!")
