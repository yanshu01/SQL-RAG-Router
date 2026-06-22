# SQL + RAG Router

An AI-powered Hybrid Query System that intelligently routes user questions to either:

- **SQLite Database** for structured employee-related queries
- **ChromaDB Vector Database** for company policy and document-based questions

The application uses a simple routing mechanism to determine whether a query should be answered using SQL or Retrieval-Augmented Generation (RAG).

---

## Features

### SQL Analytics

Ask questions such as:

- What is Sophia Jones's salary?
- Who earns the highest salary?
- Top 5 highest paid employees
- How many employees are in IT?
- List all Finance employees
- Show average salary by department
- Which department has the highest average salary?

### RAG-based Document Search

Ask questions such as:

- How many leave days are employees allowed?
- What is the company's work from home policy?
- What is the password policy?
- How does the travel reimbursement process work?

The system retrieves the most relevant document chunk from the vector database and returns the answer.

---

## Tech Stack

| Technology | Purpose |
|------------|----------|
| Python | Core Programming Language |
| Streamlit | Web Interface |
| SQLite | Structured Employee Database |
| Pandas | Data Processing & Tables |
| ChromaDB | Vector Database |
| Sentence Transformers | Text Embeddings |
| all-MiniLM-L6-v2 | Embedding Model |
| RAG | Document Retrieval |

---

## Project Structure

```text
sql-rag-router/
│
├── app.py
├── database.py
├── rag.py
├── router.py
│
├── employees.db
│
├── data/
│   ├── employees.csv
│   ├── leave_policy.txt
│   ├── hr_policy.txt
│   ├── security_policy.txt
│   ├── travel_policy.txt
│   └── benefits_policy.txt
│
├── chroma_db/
│
├── requirements.txt
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/yanshu01/SQL-RAG-Router.git

cd SQL-RAG-Router
```

### Create Virtual Environment

Mac/Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Required Dependencies

```bash
streamlit
pandas
chromadb
sentence-transformers
torch
```

Generate requirements file:

```bash
pip freeze > requirements.txt
```

---

## Build Database

Load employee data from CSV into SQLite:

```bash
python3 database.py
```

Verify:

```bash
sqlite3 employees.db
```

```sql
SELECT COUNT(*) FROM employees;
```

---

## Build Vector Database

Create embeddings and store them in ChromaDB:

```bash
python3 rag.py
```

Expected Output:

```text
Vector database created successfully!
```

---

## Run Application

```bash
streamlit run app.py
```

Application will open at:

```text
http://localhost:8501
```

---

## Example Queries

### SQL Queries

```text
What is Sophia Jones's salary?
```

```text
Who earns the highest salary?
```

```text
Top 5 highest paid employees
```

```text
List all Finance employees
```

```text
How many employees are in IT?
```

```text
Show average salary by department
```

---

### RAG Queries

```text
How many leave days are employees allowed?
```

```text
What is the company's travel policy?
```

```text
What is the password policy?
```

```text
What benefits are provided to employees?
```

---

## Routing Logic

The application first classifies the user query:

### SQL Route

Used for:

- Employee information
- Salaries
- Departments
- Counts
- Analytics

### RAG Route

Used for:

- Company policies
- HR documents
- Travel policies
- Security policies
- Benefits information

---

## Future Enhancements

- LLM-based Query Router
- Natural Language to SQL Generation
- Multi-document Retrieval
- Conversational Memory
- OpenAI/Groq Integration
- Knowledge Graph Support
- Web Search Integration

---

## Author

Yateen Sharma

Generative AI | RAG | AI Engineering | Python Development

---
