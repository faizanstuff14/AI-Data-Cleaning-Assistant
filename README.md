```# AI Data Cleaning Assistant

AI Data Cleaning Assistant is a web application that helps users automatically clean CSV datasets.
Users can upload any CSV file, and the system applies a generic, dataset-independent data-cleaning workflow to handle common real-world data issues such as missing values, mixed data types, inconsistent text, and invalid numeric values.

The project is built as a full-stack application and focuses on safe, transparent data transformations.

---

## Why I Built This

Most real-world datasets are messy. Cleaning them manually every time is slow, repetitive, and error-prone.

I built this project to create a reusable cleaning system that works on any CSV file without hardcoding column names or formats.
The goal was not to over-clean the data, but to clean it carefully while clearly explaining what was done.

---

## What This App Can Do

- Register and log in users
- Securely upload CSV files
- Automatically clean any dataset
- Handle common data issues:
  - Missing values
  - Mixed numeric and text columns
  - Inconsistent text formatting
  - Empty datasets
- Generate:
  - Cleaned CSV file
  - PDF report explaining applied cleaning steps
- Store upload history per user
- Allow users to download their cleaned files

---

## Tech Stack Used

- Backend: FastAPI
- Frontend: Streamlit
- Database: PostgreSQL
- ORM: SQLAlchemy
- Authentication: JWT (OAuth2)
- Data Processing: Pandas
- Workflow Engine: LangGraph
- PDF Reports: ReportLab

---

## Project Structure

ai_data_cleaning_assistant/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── dependencies.py
│   │
│   ├── routes/
│   │   ├── auth_routes.py
│   │   └── data_routes.py
│   │
│   ├── cleaning/
│   │   ├── schema.py
│   │   ├── numeric.py
│   │   ├── text.py
│   │   ├── missing.py
│   │   ├── workflow.py
│   │   └── report.py
│
├── frontend/
│   └── streamlit_app.py
│
├── uploads/
├── cleaned/
└── README.md

---

## How the Cleaning Works

The system does not assume anything about the dataset.

1. The CSV file is uploaded and validated
2. Columns are analyzed to infer their data types
3. Each column is cleaned based on its inferred type
4. Every transformation is recorded step-by-step
5. A cleaned CSV and a PDF summary report are generated

---

## Authentication Flow

- Users register with email and password
- Passwords are hashed securely
- Login returns a JWT access token
- All upload and download routes are protected
- Each user can only access their own files

---

## How to Run the Project

### 1. Create Environment

conda create -n ai_assistant python=3.10  
conda activate ai_assistant

### 2. Install Dependencies

pip install -r requirements.txt

### 3. Setup PostgreSQL

Create a PostgreSQL database and update the connection string in database.py.

### 4. Run Backend

uvicorn app.main:app --reload

API Docs: http://127.0.0.1:8000/docs

### 5. Run Frontend

streamlit run frontend/streamlit_app.py

---

## What This Project Focuses On

- Writing safe and generic data-cleaning logic
- Avoiding assumptions about column names
- Keeping transformations transparent
- Building a complete full-stack system
- Handling real-world messy data
```
