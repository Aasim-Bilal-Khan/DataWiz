# 🧠 DataWiz Agent

**DataWiz Agent** is an AI-powered web app that lets users interact with their MySQL databases using natural language queries (supports multiple languages, including Roman Urdu). The app uses large language models (LLMs) to generate and execute SQL queries automatically and displays results in a professional, user-friendly table format.

---

## 📦 Requirements

- Python 3.10+
- pip (Python package manager)
- MySQL Server (can use XAMPP for local setup)
- Groq API Key

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Aasim-Bilal-Khan/DataWiz.git
cd datawiz/backend
```
### 2. Set Up Virtual Environment (Recommended)

Windows
```
python -m venv env
env\Scripts\activate
```
macOS/Linux
```
python3 -m venv env
source env/bin/activate
```

### 3. Install Python Dependencies
```
pip install -r requirements.txt

```
### 4. Configure .env File

Create a .env file inside the backend/ folder with the following content:
```
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
GROQ_API_KEY=your_groq_api_key

```
# 🚀 Running the App
Start XAMPP and make sure MySQL is running.

In your terminal:

cd backend
python main.py

Your default browser will open at http://127.0.0.1:5000

# 🧠 Features
Accepts user input in multiple languages (auto-translates to English)

Uses Groq-hosted LLMs to generate SQL

Runs real SQL queries on your MySQL database

Returns data in clean tabular format

Copy generated queries with one click

Fully responsive, modern frontend (TailwindCSS)


# 📜 License

Copyright (c) 2025 Aasim-Bilal-Khan
This project is not for commercial use.
All rights reserved.
