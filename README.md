# 🚀 AI Resume Agent

An AI-powered resume optimization and job application assistant.

This project helps users:
- Optimize resumes using AI
- Improve ATS scores
- Generate tailored resumes
- Download optimized resumes
- Apply via email
- Launch LinkedIn Easy Apply with human-in-the-loop safety

---

## ✨ Features

- 📄 Resume optimization (PDF / DOCX)
- 🧠 AI-driven content rewriting
- 📊 ATS score & missing keyword analysis
- 🎨 Multiple resume designs (minimal / modern / premium)
- 🧩 Resume density control (compact / detailed)
- 📥 Download optimized resume
- 📧 Auto-apply via email
- 🔗 LinkedIn Easy Apply launcher (assisted)
- 🛡 Human approval & safety gates

---

## 🧱 Tech Stack

### Backend
- FastAPI
- Python 3.9+
- Playwright (LinkedIn assisted apply)
- LangChain + LLM (local or hosted)
- PDF / DOCX parsing

### Frontend
- React
- Fetch API
- Minimal UI (easy to extend)

---

## 📂 Project Structure

```
resume-agent/
│
├── backend/
│   ├── main.py
│   ├── utils/
│   ├── agent/
│   ├── ats/
│   ├── linkedin/
│   ├── resumes/
│   │   └── optimized/
│   └── config.py
│
├── frontend/
│   ├── src/
│   └── package.json
│
├── .gitignore
├── README.md
```

---

## ⚙️ Backend Setup

### 1️⃣ Create virtual environment
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run backend
```bash
uvicorn main:app --reload
```

Backend will start at:
```
http://localhost:8000
```

---

## 🌐 Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend runs at:
```
http://localhost:3000
```

---

## ⬇️ Download Optimized Resume

After optimization, resumes are downloadable at:
```
http://localhost:8000/resumes/optimized/<filename>
```

A **Download Optimized Resume** button is available in the UI.

---

## 🔗 LinkedIn Easy Apply (Assisted)

- Launches LinkedIn job page
- Uploads resume automatically
- User completes remaining steps manually
- Browser stays open for safety
- No ToS-breaking automation

---

## 🔐 Configuration Flags

Edit `backend/config.py`:

```python
AUTO_APPLY_ENABLED = False
HUMAN_APPROVAL_REQUIRED = True
```

---

## ⚠️ Important Notes

- This tool does **not** auto-submit LinkedIn applications
- Designed for **human-in-the-loop safety**
- Avoids CAPTCHA and account bans
- Generated resumes are ignored by git (not pushed)

---

## 🛣 Roadmap

- Job scraping & ranking
- Resume versioning per job
- Application tracking dashboard
- S3 resume storage
- Multi-user authentication

---

## 📜 License

AR License

---

## 🙌 Author

Built with ❤️ as an AI-powered career assistant.
