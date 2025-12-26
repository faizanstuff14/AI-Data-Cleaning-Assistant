# AI-Data-Cleaning-Assistant
This project is a web application that helps users clean CSV datasets automatically.
Users can upload any CSV file, and the system applies a generic data-cleaning workflow to handle common real-world data issues like missing values, mixed data types, inconsistent text, and invalid numeric values.

The project includes:

A FastAPI backend

A Streamlit frontend

JWT authentication

PostgreSQL for storing users and upload history

Why I Built This

Most datasets are messy, and cleaning them manually every time is slow and repetitive.
This project was built to create a reusable, dataset-independent cleaning system that works on any CSV file without hardcoding column names or formats.

The goal was not to over-clean the data, but to clean it safely and transparently.

What This App Can Do

Register and log in users

Upload CSV files securely

Automatically clean any dataset

Handle:

Missing values

Mixed numeric/text columns

Inconsistent text formatting

Empty datasets

Generate:

Cleaned CSV file

PDF report explaining what cleaning steps were applied

Store upload history per user

Allow users to download their cleaned files

Tech Stack Used

Backend: FastAPI

Frontend: Streamlit

Database: PostgreSQL

ORM: SQLAlchemy

Authentication: JWT (OAuth2)

Data Processing: Pandas

Workflow Engine: LangGraph

PDF Reports: ReportLab

Project Structure
ai_data_cleaning_assistant/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── dependencies.py
│
│   ├── routes/
│   │   ├── auth_routes.py
│   │   └── data_routes.py
│
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

How the Cleaning Works

The system does not assume anything about the dataset.

The CSV is uploaded and validated

The columns are analyzed to infer their types

Each column is cleaned based on its inferred type:

Numeric values are safely converted

Text is normalized (lowercase, trimmed)

Missing values are handled carefully

Every step is recorded so the user can see what happened

The cleaned dataset and a PDF summary are generated

Authentication Flow

Users register with email and password

Passwords are hashed securely

Login returns a JWT access token

All data upload and download routes are protected

Each user only sees their own files

How to Run the Project
1. Create Environment
conda create -n ai_assistant python=3.10
conda activate ai_assistant

2. Install Dependencies
pip install -r requirements.txt

3. Setup PostgreSQL

Create a database and update the connection string in database.py.

4. Run Backend
uvicorn app.main:app --reload


API Docs:

http://127.0.0.1:8000/docs

5. Run Frontend
streamlit run frontend/streamlit_app.py

What This Project Focuses On

Writing safe data cleaning logic

Avoiding assumptions about column names

Keeping transformations transparent

Building a full-stack system, not just scripts

Handling real-world messy data

Known Limitations

No AI-based prediction or imputation

No automatic semantic understanding of columns

Cleaning is conservative by design

These were intentional choices to avoid damaging data.

Future Improvements

Preview cleaned data in the UI

Download history page

More detailed column-level reports

Deployment to cloud

Final Notes

This project was built step by step with a focus on clarity, correctness, and real-world usability.
It is meant to be understandable, extensible, and safe — not a black-box cleaner.
