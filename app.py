from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import re

app = Flask(__name__)
app.secret_key = "datamasking_secret_2025"

# ── User store ──────────────────────────────────────────────────────────────
USERS = {
    "admin":   {"password": "admin123",   "role": "Admin"},
    "analyst": {"password": "analyst123", "role": "Analyst"},
    "viewer":  {"password": "viewer123",  "role": "Viewer"},
}

# ── Employee dataset ─────────────────────────────────────────────────────────
EMPLOYEES = [
    {"id": 1,  "name": "Amal Perera",      "email": "amal.perera@corp.lk",    "nic": "199012345678", "salary": 185000, "department": "Engineering",  "role_title": "Senior Engineer"},
    {"id": 2,  "name": "Dilani Fernando",  "email": "dilani.f@corp.lk",       "nic": "198756781234", "salary": 210000, "department": "Finance",       "role_title": "Finance Manager"},
    {"id": 3,  "name": "Kasun Silva",      "email": "kasun.silva@corp.lk",    "nic": "200034567890", "salary": 95000,  "department": "HR",            "role_title": "HR Coordinator"},
    {"id": 4,  "name": "Nimesha Jayawardena", "email": "nimesha.j@corp.lk",  "nic": "199567892345", "salary": 155000, "department": "Engineering",  "role_title": "DevOps Engineer"},
    {"id": 5,  "name": "Ruwan Bandara",    "email": "ruwan.b@corp.lk",        "nic": "198845671234", "salary": 320000, "department": "Management",   "role_title": "CTO"},
    {"id": 6,  "name": "Sachini Kumari",   "email": "sachini.k@corp.lk",      "nic": "200112348765", "salary": 88000,  "department": "Support",      "role_title": "Support Analyst"},
    {"id": 7,  "name": "Tharaka Madusanka","email": "tharaka.m@corp.lk",      "nic": "199723456789", "salary": 125000, "department": "Engineering",  "role_title": "Software Engineer"},
    {"id": 8,  "name": "Upeksha Rathnayake","email": "upeksha.r@corp.lk",     "nic": "199834561230", "salary": 145000, "department": "Finance",      "role_title": "Accountant"},
    {"id": 9,  "name": "Vimukthi Gunasekara","email": "vimukthi.g@corp.lk",   "nic": "200256783456", "salary": 78000,  "department": "Support",     "role_title": "Support Analyst"},
    {"id": 10, "name": "Yasoda Liyanage",  "email": "yasoda.l@corp.lk",       "nic": "199067891234", "salary": 265000, "department": "Management",  "role_title": "Head of HR"},
]

# ── Masking helpers ───────────────────────────────────────────────────────────
def mask_email(email):
    local, domain = email.split("@")
    return local[0] + "***@" + domain[0] + "***"

def mask_nic(nic):
    return nic[:3] + "-" + "*" * 6 + "-" + nic[-1]

def mask_salary():
    return "*** RESTRICTED ***"

# ── Role-based masking policy ─────────────────────────────────────────────────
# Each role defines which fields to mask
MASKING_POLICY = {
    "Admin":   {"email": False, "nic": False,  "salary": False},
    "Analyst": {"email": False, "nic": True,   "salary": False},
    "Viewer":  {"email": True,  "nic": True,   "salary": True},
}

def apply_masking(employee, role):
    policy = MASKING_POLICY.get(role, MASKING_POLICY["Viewer"])
    masked = dict(employee)
    masked["email"]  = mask_email(employee["email"])  if policy["email"]  else employee["email"]
    masked["nic"]    = mask_nic(employee["nic"])       if policy["nic"]    else employee["nic"]
    masked["salary"] = mask_salary()                   if policy["salary"] else f"Rs. {employee['salary']:,}"
    masked["masked_fields"] = [f for f, m in policy.items() if m]
    return masked

# ── Routes ────────────────────────────────────────────────────────────────────
@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")
        user = USERS.get(username)
        if user and user["password"] == password:
            session["username"] = username
            session["role"]     = user["role"]
            return redirect(url_for("dashboard"))
        error = "Invalid username or password."
    return render_template("login.html", error=error)

@app.route("/dashboard")
def dashboard():
    if "role" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html",
                           username=session["username"],
                           role=session["role"],
                           policy=MASKING_POLICY[session["role"]])

@app.route("/query")
def query():
    if "role" not in session:
        return redirect(url_for("login"))

    role       = session["role"]
    search     = request.args.get("search", "").strip().lower()
    department = request.args.get("department", "").strip()

    results = EMPLOYEES
    if search:
        results = [e for e in results if search in e["name"].lower()
                   or search in e["department"].lower()
                   or search in e["role_title"].lower()]
    if department and department != "All":
        results = [e for e in results if e["department"] == department]

    masked_results = [apply_masking(e, role) for e in results]
    departments    = sorted(set(e["department"] for e in EMPLOYEES))
    policy         = MASKING_POLICY[role]

    return render_template("dashboard.html",
                           username=session["username"],
                           role=role,
                           results=masked_results,
                           search=search,
                           selected_dept=department,
                           departments=departments,
                           policy=policy,
                           total=len(masked_results))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
