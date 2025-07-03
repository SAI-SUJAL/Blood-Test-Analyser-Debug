Here's a cleaned-up, professional, and more readable version of your README with the improvements and specific challenges you faced clearly addressed:

---

# 🧪 Blood Test Analyser API

A **FastAPI-based AI application** that analyzes blood test reports and provides personalized health recommendations using autonomous AI agents.

---

## 🚀 Features

* 📄 Upload & analyze blood test PDF reports
* 🧠 AI-powered health insights & suggestions
* 🔄 Asynchronous processing for better performance
* 🌐 RESTful API with interactive Swagger documentation
* ⚙️ Modular agent, task, and tool design using CrewAI

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/blood-test-analyser-debug.git
cd blood-test-analyser-debug
```

### 2. Install Dependencies

> ⚠️ Dependency management has been cleaned up. Previously, tool misconfiguration and incompatible versions caused crashes. Now works with:

```bash
pip install -r requirements.txt
pip install fastapi uvicorn crewai
```

### 3. Environment Setup

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Update your `.env` with your Groq API Key:

```
GROQ_API_KEY=your_groq_api_key_here
```

> 🔐 *Do not commit your `.env` file.*

---

### 4. Run the Application

```bash
uvicorn main:app --reload
```

* The app will be available at:
  📍 [http://localhost:8000](http://localhost:8000)

---

## 🧪 API Endpoints

### ✅ Health Check

**GET /**
Checks if the API is live.
**Response:**

```json
{
  "message": "Blood Test Report Analyser API is running"
}
```

---

### 🧾 Analyze Blood Test Report

**POST /analyze**

Upload a blood test **PDF** and receive health insights.

**Request Parameters:**

| Param | Type   | Required | Description                       |
| ----- | ------ | -------- | --------------------------------- |
| file  | `PDF`  | ✅        | Your blood test report file       |
| query | string | ❌        | Optional custom analysis question |

**Example Response:**

```json
{
  "status": "success",
  "query": "Summarise my Blood Test Report",
  "analysis": "Recommendations and insights...",
  "file_processed": "blood_test.pdf",
  "file_size": 112345
}
```

---

## 🧪 Testing the API

### 📘 Swagger UI

Visit [http://localhost:8000/docs](http://localhost:8000/docs) for an interactive Swagger interface.

---

### 🧵 Using `curl`:

```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_blood_test.pdf" \
  -F "query=Analyze my cholesterol levels"
```

---

## 🛠️ Recent Fixes & Improvements

> While building this project, the following challenges were encountered and resolved:

| Area                    | Fixes Applied                                     |
| ----------------------- | ------------------------------------------------- |
| 🔁 **Dependencies**     | Fixed broken or redundant packages                |
| 🤖 **Agents & Prompts** | Rewrote ineffective prompts and agent logic       |
| 🛠️ **Tools**           | Rebuilt misconfigured tools with clean logic      |
| 📋 **Task Prompts**     | Refined and clarified prompts for better output   |
| 🔄 **Async Issues**     | Added missing `await` statements in async flows   |
| 🧠 **Tool Logic**       | Cleaned up functions for stability and modularity |
| 🔂 **Max Iterations**   | Controlled runaway loops in CrewAI configurations |

---

## 📦 Requirements

* Python 3.8+
* FastAPI
* Uvicorn
* CrewAI
* Groq API Key (from [Groq Console](https://console.groq.com))
* All dependencies in `requirements.txt`

---

## 📄 License

MIT

---

Let me know if you want a badge section, project structure diagram, or deployment instructions (e.g., with Docker or Railway).
