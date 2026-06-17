# DataGuard — Role-Based Data Masking & Secure Query Platform

A web application that demonstrates **data privacy enforcement** through role-based access control (RBAC) and automatic PII masking. Built as a portfolio project to demonstrate practical data privacy and governance concepts.

---

## What it does

Users authenticate and query an employee database, but **sensitive PII fields are automatically masked** based on the user's assigned role — enforcing the principle of least privilege at the data layer.

| Field      | Admin     | Analyst          | Viewer            |
|------------|-----------|------------------|-------------------|
| Name       | ✅ Full   | ✅ Full          | ✅ Full           |
| Email      | ✅ Full   | ✅ Full          | ⬛ ma***@d***.com |
| NIC        | ✅ Full   | ⬛ 199-******-8  | ⬛ 199-******-8   |
| Salary     | ✅ Full   | ✅ Full          | ⬛ RESTRICTED     |
| Department | ✅ Full   | ✅ Full          | ✅ Full           |

---

## Privacy & Compliance concepts demonstrated

- **Data minimisation** — users only see what their role requires
- **PII masking** — NIC, email, and salary masked using format-preserving techniques
- **Role-Based Access Control (RBAC)** — three-tier access policy (Admin / Analyst / Viewer)
- **Query audit logging** — every query is logged with user, role, and masking policy applied
- **Data governance policy enforcement** — centralised masking policy, not scattered across queries
- **Least privilege principle** — viewers cannot access salary or full PII

---

## Tech stack

- **Backend**: Python 3.x + Flask
- **Frontend**: HTML5, CSS3 (no frameworks)
- **Data store**: In-memory (easily replaceable with PostgreSQL/MySQL)

---

## Setup & run

```bash
# 1. Clone / download the project
cd data_masking_app

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py

# 4. Open in browser
http://localhost:5000
```

---

## Demo credentials

| Username  | Password    | Role    |
|-----------|-------------|---------|
| admin     | admin123    | Admin   |
| analyst   | analyst123  | Analyst |
| viewer    | viewer123   | Viewer  |

---

## CV project description (ready to paste)

**Data Masking & Secure Query Platform** *(2025)*  
Designed and developed a role-based data privacy enforcement system in Python (Flask) that automatically masks PII fields (NIC, email, salary) based on a user's assigned role at query time. Implemented a centralised masking policy engine supporting Admin, Analyst, and Viewer access tiers. Demonstrated core data governance concepts including data minimisation, least privilege, and query audit logging — aligned with GDPR and data protection best practices.  
*Technologies: Python, Flask, RBAC, PII Masking, Data Governance*

---

## Project structure

```
data_masking_app/
├── app.py              # Flask app, masking engine, routing
├── requirements.txt
├── README.md
└── templates/
    ├── login.html      # Authentication UI
    └── dashboard.html  # Query interface with masked results
```
