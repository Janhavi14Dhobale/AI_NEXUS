# AI_NEXUS – AI Code Reviewer 🚀

AI_NEXUS is a static code analysis tool that helps developers detect **bugs, security vulnerabilities, and performance issues** in their code.
The tool analyzes source code and provides **clear explanations and suggested fixes** to improve code quality.

This project was built as a demonstration of how AI-assisted tools can help developers write **safer and more efficient programs**.

---

## ✨ Features

* 🔍 Detects **syntax errors**
* ⚠️ Identifies **division by zero**
* 🔁 Detects **infinite loops**
* 🧠 Finds **mutable default argument issues**
* 🚫 Detects **bare except blocks**
* 🔐 Identifies **hardcoded passwords**
* ⚡ Detects **nested loops with possible O(n²) complexity**
* 🧹 Finds **unused variables**
* 🛑 Detects **unsafe eval() usage**
* 📊 Shows **code complexity information**
* 💡 Provides **explanations and suggested fixes**

---

## 🏗 Project Architecture

Frontend (React)
⬇
API Request
⬇
Backend (FastAPI)
⬇
Python AST Analysis Engine
⬇
Results (Bugs + Security + Complexity)

---

## 🛠 Tech Stack

### Frontend

* React
* Axios
* CSS

### Backend

* FastAPI
* Python
* AST (Abstract Syntax Tree)

---

## 📂 Project Structure

```
AI_NEXUS
│
├── backend
│   ├── main.py
│   ├── analyzer.py
│
├── frontend
│   ├── src
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── App.css
│
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Janhavi14Dhobale/AI_NEXUS.git
cd AI_NEXUS
```

---

### 2️⃣ Start Backend

```
cd backend
pip install fastapi uvicorn
uvicorn main:app --reload
```

Backend runs on:

```
http://127.0.0.1:8000
```

---

### 3️⃣ Start Frontend

```
cd frontend
npm install
npm run dev
```

Frontend runs on:

```
http://localhost:5173
```

---

## 🧪 Example Code for Testing

```
password = "1234"

x = 10
y = 0

unused = 5

while True:
    print(x / y)

eval("print('danger')")
```

The analyzer will detect:

* Hardcoded password
* Division by zero
* Infinite loop
* Unused variable
* Unsafe eval usage

---

## 🎯 Future Improvements

* Multi-language support (Java, JavaScript)
* AI-based code suggestions
* GitHub integration
* Advanced complexity analysis
* Real-time code scanning

---
