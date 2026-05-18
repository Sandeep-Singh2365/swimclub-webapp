Online Link - https://sandeepsingh6565.pythonanywhere.com/
# Swim Club Analytics Web Application

A Flask-based Swim Club Analytics Web App that allows users to explore swimmer performance data, analyze event timings, and compare results against world records using interactive visualizations.

---

# Features

- View swim session dates
- Browse swimmers participating in a session
- Explore swimming events
- Analyze swimmer timings
- Compare against world records
- Bar-chart based performance visualization
- MySQL database integration
- Environment-variable based configuration

---

# Tech Stack

## Backend
- Python
- Flask

## Database
- MySQL / MariaDB
- PyMySQL

## Frontend
- HTML
- CSS
- Jinja2 Templates

## Other Tools
- python-dotenv
- statistics module

---

# Project Structure

```text
webapp/
│
├── app.py                 # Main Flask application
├── data_utils.py          # Database/data handling utilities
├── convert_utils.py       # Time conversion and analytics logic
├── queries.py             # SQL queries
├── dbcm.py                # Database context manager
├── data.sql               # Database schema/data
├── records.json           # World record dataset
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── select.html
│   └── chart.html
│
├── static/
│   └── webapp.css
│
└── swimdata/
