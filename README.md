<div align="center">

# 🎓 AcadAI

### Multi-Agent RAG Powered Academic Learning Assistant

*An intelligent AI-powered academic assistant built using LangGraph, LangChain, Retrieval-Augmented Generation (RAG), and Large Language Models to provide personalized learning support.*

<br>

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Framework-00C853?style=for-the-badge)
![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-7B1FA2?style=for-the-badge)
![FAISS](https://img.shields.io/badge/FAISS-VectorDB-FF9800?style=for-the-badge)
![MongoDB](https://img.shields.io/badge/MongoDB-Database-47A248?style=for-the-badge&logo=mongodb&logoColor=white)

![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![AI](https://img.shields.io/badge/AI-Generative_AI-purple?style=for-the-badge)

</div>

---

# 🌟 Overview

AcadAI is a **Multi-Agent Academic Learning Assistant** that combines **Large Language Models (LLMs)**, **Retrieval-Augmented Generation (RAG)**, and **LangGraph-based agent orchestration** to provide intelligent academic support.

Instead of relying on a single chatbot, AcadAI routes user requests through specialized AI agents capable of answering academic questions, generating quizzes, creating study plans, summarizing educational content, and retrieving context-aware information from institutional documents.

The system ensures that every response is grounded in uploaded academic resources through a robust Retrieval-Augmented Generation (RAG) pipeline powered by semantic search.

---

# 🚀 Key Highlights

- 🤖 Multi-Agent Architecture using LangGraph
- 📚 Retrieval-Augmented Generation (RAG)
- 🔎 Semantic Search using FAISS Vector Database
- 🧠 Context-Aware Academic Question Answering
- 📄 Intelligent PDF & Document Processing
- 📝 AI-powered Quiz Generation
- 📅 Personalized Study Planner
- 📑 Automatic Academic Summarization
- 💾 Conversation Memory & Chat History
- 📚 Citation-aware Response Generation
- ⚡ Modular and Scalable Architecture

---

# ✨ Features

| Feature | Description |
|----------|-------------|
| 🤖 Multi-Agent System | Specialized agents coordinated by LangGraph Supervisor |
| 📚 Academic QA | Context-aware question answering using RAG |
| 📝 Quiz Generator | Automatically creates MCQs and subjective questions |
| 📄 Smart Summarizer | Generates concise chapter and topic summaries |
| 📅 Study Planner | Builds personalized study schedules |
| 🔍 Semantic Search | Retrieves relevant academic content using FAISS |
| 💾 Memory | Stores chat history and conversation context |
| 📊 Dashboard | Tracks learning progress and interactions |
| 📑 Citation Support | Generates source-aware academic responses |

---

# 🏗️ System Architecture

> **High-Level Architecture**

<p align="center">

![System Architecture](assets/system_architecture.png)

</p>

---

# 🤖 Multi-Agent Workflow

> **LangGraph Agent Orchestration**

<p align="center">

![Multi-Agent Workflow](assets/multi_agent_workflow.png)

</p>

---

# 📚 Retrieval-Augmented Generation (RAG)

> **Academic Retrieval Pipeline**

<p align="center">

![RAG Pipeline](assets/rag_pipeline.png)

</p>

---

# ⚙️ Technology Stack

## Frontend

- Streamlit

## Backend

- Python

## AI Framework

- LangChain
- LangGraph

## Vector Database

- FAISS

## Database

- MongoDB

## Large Language Models

- OpenAI GPT
- Mistral
- Ollama

## NLP & Embeddings

- Sentence Transformers
- HuggingFace
- NLTK

## OCR

- EasyOCR
- Tesseract OCR

## Utilities

- Pandas
- NumPy
- PyPDF
- python-dotenv

---

# 📂 Project Structure

```text
AcadAI/
│
├── app.py                     # Streamlit application entry point
├── main.py                    # Application bootstrap
├── config.py                  # Configuration settings
├── requirements.txt           # Project dependencies
├── .env.example               # Environment variables template
├── README.md
│
├── agents/                    # Multi-Agent implementations
│   ├── supervisor.py
│   ├── qa_agent.py
│   ├── quiz_agent.py
│   ├── planner_agent.py
│   ├── summarizer_agent.py
│   └── citation_agent.py
│
├── ingestion/                 # Document ingestion pipeline
│
├── retrieval/                 # Hybrid RAG retrieval
│
├── knowledge_base/            # Vector indexing & document store
│
├── memory/                    # Conversation memory
│
├── llm/                       # LLM providers & routing
│
├── models/                    # Embedding & ML models
│
├── tools/                     # Helper utilities
│
├── ui/                        # Streamlit UI components
│
├── assets/
│   ├── logo.png
│   ├── system_architecture.png
│   ├── rag_pipeline.png
│   ├── multi_agent_workflow.png
│   ├── dashboard.png
│   ├── chat.png
│   ├── upload.png
│   └── demo.gif
│
├── uploads/
│
└── documents/
```

> **Note:** Update this structure to exactly match your repository before publishing.

---

# 🚀 Getting Started

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/AcadAI.git
```

```bash
cd AcadAI
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv .venv
```

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Configure Environment Variables

Create a file named

```text
.env
```

Example:

```env
OPENAI_API_KEY=your_openai_api_key

MONGODB_URI=your_mongodb_connection_string

MODEL_PROVIDER=openai

MODEL_NAME=gpt-4o

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

VECTOR_DB=faiss
```

---

## 5️⃣ Launch AcadAI

```bash
streamlit run app.py
```

The application will start on

```text
http://localhost:8501
```

---

# 💻 Usage

### Academic Question Answering

Ask questions from uploaded academic documents.

```
Explain Retrieval-Augmented Generation.
```

---

### Quiz Generation

Generate quizzes from notes or uploaded PDFs.

```
Generate 15 MCQs from Unit 3.
```

---

### Study Planner

Create personalized study schedules.

```
Prepare a 7-day study plan for Machine Learning.
```

---

### Summarization

Generate concise chapter summaries.

```
Summarize this chapter into key points.
```

---

### Smart Search

Retrieve context-aware answers from institutional documents.

```
What topics are covered in Module 4?
```

---

# 📸 Application Screenshots

## Dashboard

<p align="center">

<img src="assets/dashboard.png" width="900">

</p>

---

## AI Chat Interface

<p align="center">

<img src="assets/chat.png" width="900">

</p>

---

## Document Upload

<p align="center">

<img src="assets/upload.png" width="900">

</p>

---

## Quiz Generator

<p align="center">

<img src="assets/quiz.png" width="900">

</p>

---

## Study Planner

<p align="center">

<img src="assets/planner.png" width="900">

</p>

---

# 🎥 Demo

> Replace the placeholder below with an animated GIF or a short demo video.

<p align="center">

<img src="assets/demo.gif" width="900">

</p>

---

# 📦 Supported Document Types

| Format | Supported |
|---------|-----------|
| PDF | ✅ |
| DOCX | ✅ |
| PPTX | ✅ |
| TXT | ✅ |
| Markdown | ✅ |
| Lecture Notes | ✅ |
| Assignments | ✅ |
| Research Papers | ✅ |

---

# 🔐 Environment Variables

| Variable | Description |
|----------|-------------|
| OPENAI_API_KEY | OpenAI API key |
| MONGODB_URI | MongoDB connection string |
| MODEL_PROVIDER | LLM provider |
| MODEL_NAME | Selected LLM |
| VECTOR_DB | FAISS / ChromaDB |
| EMBEDDING_MODEL | Embedding model name |

---

# 📊 Project Workflow

```text
                Student
                    │
                    ▼
          Streamlit Web Interface
                    │
                    ▼
          LangGraph Supervisor
                    │
        Intent Detection & Routing
                    │
      ┌─────────────┼─────────────┐
      ▼             ▼             ▼
 Academic QA    Quiz Agent    Planner Agent
      │             │             │
      └─────────────┼─────────────┘
                    ▼
              RAG Pipeline
                    │
         FAISS + MongoDB Retrieval
                    │
            Context Construction
                    │
               Prompt Builder
                    │
              LLM (GPT/Ollama)
                    │
                    ▼
            Context-Aware Response
                    │
                    ▼
                 Student
```

---

# 📈 Performance & Capabilities

| Capability | Status |
|------------|:------:|
| Multi-Agent Architecture | ✅ |
| Retrieval-Augmented Generation (RAG) | ✅ |
| Semantic Search | ✅ |
| FAISS Vector Retrieval | ✅ |
| MongoDB Metadata Storage | ✅ |
| Context-Aware Responses | ✅ |
| Conversation Memory | ✅ |
| Intelligent Quiz Generation | ✅ |
| Personalized Study Planner | ✅ |
| Automatic Summarization | ✅ |
| Citation Generation | ✅ |
| PDF Knowledge Base | ✅ |

---

# 🛣️ Roadmap

## ✅ Current Features

- Multi-Agent Framework
- LangGraph Orchestration
- Retrieval-Augmented Generation
- Semantic Search
- Academic Question Answering
- Quiz Generation
- Study Planner
- Smart Summarization
- PDF Upload & Processing
- Conversation Memory

---

## 🚧 Upcoming Features

- Voice-based Academic Assistant
- AI Tutor with Interactive Sessions
- OCR Support for Scanned Documents
- Hybrid Search (BM25 + Vector Search)
- Multi-language Support
- Personalized Learning Analytics
- LMS Integration
- Mobile Application
- Admin Dashboard
- Collaborative Learning Workspace

---

# 🧪 Technologies Used

| Category | Technologies |
|----------|--------------|
| Programming Language | Python |
| Frontend | Streamlit |
| AI Framework | LangChain, LangGraph |
| Retrieval | FAISS |
| Database | MongoDB |
| LLM | OpenAI GPT, Ollama, Mistral |
| Embeddings | Sentence Transformers |
| NLP | NLTK, HuggingFace |
| OCR | EasyOCR, Tesseract |
| Version Control | Git, GitHub |

---

# 🤝 Contributing

Contributions are welcome!

If you would like to improve AcadAI:

1. Fork the repository.
2. Create a new feature branch.

```bash
git checkout -b feature/your-feature-name
```

3. Commit your changes.

```bash
git commit -m "Add new feature"
```

4. Push your branch.

```bash
git push origin feature/your-feature-name
```

5. Open a Pull Request.

---

# 🧩 Future Research Directions

AcadAI can be extended with:

- Agentic Planning using advanced LangGraph workflows
- GraphRAG for relationship-aware retrieval
- Adaptive Learning Recommendation Systems
- Multi-modal Learning (Text + Images + Audio)
- Reinforcement Learning from Student Feedback
- Institution-wide Knowledge Graph Integration

---

# 📜 License

This project is licensed under the **MIT License**.

See the **LICENSE** file for more details.

---

# 🙏 Acknowledgements

This project builds upon the following technologies and open-source communities:

- LangChain
- LangGraph
- Streamlit
- FAISS
- MongoDB
- Hugging Face
- OpenAI
- Ollama
- Mistral AI

Special thanks to the open-source AI community for developing tools that make intelligent academic assistants possible.

---

# 👨‍💻 Author

<div align="center">

## **Shashwat Tiwari**

**B.Tech Computer Science Engineering**

Pranveer Singh Institute of Technology (PSIT), Kanpur

**AI • GenAI • RAG • Multi-Agent Systems • Machine Learning**

</div>

---

<div align="center">

## ⭐ If you found this project useful...

### Please consider giving it a ⭐ on GitHub!

It helps others discover the project and motivates future improvements.

</div>

---

<div align="center">

### 🎓 Built with ❤️ for smarter academic learning using Generative AI.

</div>
