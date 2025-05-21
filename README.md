# 🚀 Explainify

**Explainify** is a dual-tone AI explainer and summarizer web app. Instantly generate both casual and academic explanations for any topic, and get polished summaries—all powered by advanced language models.

---

## 🛠️ How to Run This Project

### 1️⃣ Clone this repository

git clone https://github.com/KingElessar007/Explainify.git
cd Explainify

---

### 2️⃣ Create and activate a Conda virtual environment

conda create -p venv python=3.12
conda activate ./venv

---

### 3️⃣ Install Python dependencies

pip install -r requirements.txt


---

### 4️⃣ Set up PostgreSQL

- **Install PostgreSQL** if you haven’t already.
- **Start the PostgreSQL server.**
- **Create a new database** (e.g., named `ai_responses`).

---

### 5️⃣ Configure environment variables

- Open the `.env` file.
- Add your database username, password, and database name.  
Example:  
DATABASE_URL=postgresql://your_username:your_password@localhost:5432/ai_responses

---

### 6️⃣ Start the backend server

uvicorn app.main:app --reload


---

### 7️⃣ Run the Streamlit app

streamlit run app/streamlit_app.py


---

### 🌐 Open your browser

Go to [http://localhost:8501](http://localhost:8501) to use the app!

---








