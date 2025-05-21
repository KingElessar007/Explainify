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

## 🧑‍💻 Tech Stack

- **Python 3.12** — Core programming language
- **FastAPI** — Backend API framework
- **Streamlit** — Interactive frontend
- **Transformers (Hugging Face)** — For AI model inference (e.g., FLAN-T5,BART-Large-CNN)
- **PostgreSQL** — Database for storing queries and summaries
- **SQLAlchemy** — ORM for database operations

---

## 📝 Prompt Strategies

- **Role-based prompts:** Assigns personas (friendly assistant, scholarly expert) to guide tone.
- **Explicit instructions:** Clearly states the task and desired format for each response.
- **Structured output:** Requests specific output formats (e.g., paragraph count, summary length).
- **Self-refinement:** Uses additional prompts for polishing and summarizing responses.

*Example (Casual):*
You're a helpful assistant who explains things like you're talking to a friend.
Instruction:
<user prompt>
Respond in 4-5 big paragraphs.

*Example (Academic):*
You're a scholarly assistant with expertise in academic writing.
Instruction:
<user prompt>
Respond in 4-5 well-developed paragraphs.
![WhatsApp Image 2025-05-21 at 22 29 50_686960b8](https://github.com/user-attachments/assets/1014154f-6b2d-4a7d-b1b1-92f1ffac1894)

## 🖼️ Screenshot
*User logs in, enters a query, and receives both casual and academic summaries after loading is finished.*

![WhatsApp Image 2025-05-21 at 22 30 32_0628842e](https://github.com/user-attachments/assets/c18ed54f-c514-4b72-8390-16bdfe9711fb)

## 🖼️ App Screenshot

*We can see both the summaries and also the history log on the left side*







