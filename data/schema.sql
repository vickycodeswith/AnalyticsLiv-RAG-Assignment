-- NovaTech Solutions sample database. Fictional data created for the AnalyticsLiv assignment.
PRAGMA foreign_keys = ON;
CREATE TABLE projects (project_id INTEGER PRIMARY KEY, project_name TEXT NOT NULL, business_unit TEXT NOT NULL, budget_usd INTEGER NOT NULL, status TEXT NOT NULL, start_date TEXT NOT NULL, target_date TEXT NOT NULL);
CREATE TABLE employees (employee_id INTEGER PRIMARY KEY, full_name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, role TEXT NOT NULL, location TEXT NOT NULL, project_id INTEGER NOT NULL, hire_date TEXT NOT NULL, FOREIGN KEY (project_id) REFERENCES projects(project_id));
CREATE TABLE support_tickets (ticket_id INTEGER PRIMARY KEY, employee_id INTEGER NOT NULL, category TEXT NOT NULL, priority TEXT NOT NULL, status TEXT NOT NULL, created_date TEXT NOT NULL, resolution_hours REAL, summary TEXT NOT NULL, FOREIGN KEY (employee_id) REFERENCES employees(employee_id));
