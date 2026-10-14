````markdown
# SQLGenAI

## Natural Language to SQL using Fine-Tuned LLMs

SQLGenAI is an AI-powered Natural Language to SQL system that converts
natural language questions into SQL queries using a fine-tuned
Qwen2.5-Coder language model.

The generated SQL is validated for safety, executed against a PostgreSQL
database, and the query results are returned through a FastAPI REST API.

---

## Project Overview

Traditional database systems require users to know SQL before they can
retrieve information from a database.

SQLGenAI allows users to interact with a database using natural language.

For example:

User:

> Show the top 5 employees with the highest salary.

SQLGenAI generates:

```sql
SELECT name FROM employees ORDER BY salary DESC LIMIT 5;
```
````

The query is validated and executed against PostgreSQL, and the results
are returned to the user.

---

## Architecture

```text
                    User Question
                         |
                         v
                   FastAPI API
                         |
                         v
              Fine-Tuned Qwen Model
              Qwen2.5-Coder-0.5B
                         |
                         v
                   SQL Generation
                         |
                         v
                   SQL Validator
                         |
                         v
                     PostgreSQL
                         |
                         v
                    Query Result
                         |
                         v
                    API Response
```

---

## Key Features

- Natural Language to SQL generation
- Fine-tuned Qwen2.5-Coder model
- LoRA-based parameter-efficient fine-tuning
- Hugging Face Transformers
- PEFT
- PostgreSQL integration
- SQL validation
- FastAPI REST API
- Swagger API documentation
- Docker containerization
- Environment-based configuration
- Local model inference

---

## Tech Stack

### AI / Machine Learning

- Python
- PyTorch
- Hugging Face Transformers
- Qwen2.5-Coder
- PEFT
- LoRA

### Backend

- FastAPI
- Uvicorn
- Pydantic

### Database

- PostgreSQL
- psycopg2

### Infrastructure

- Docker
- Docker Desktop

### Data Processing

- Pandas
- Scikit-learn
- Hugging Face Datasets

---

## Model

### Base Model

```text
Qwen/Qwen2.5-Coder-0.5B-Instruct
```

The project initially experimented with a larger Qwen2.5-Coder model,
but the 0.5B model was selected for efficient local inference.

---

## Fine-Tuning

The model was fine-tuned using **LoRA (Low-Rank Adaptation)** through
the Hugging Face PEFT library.

LoRA allows the project to adapt the language model without updating
all of its parameters.

### Training Configuration

```text
LoRA Rank: 8
LoRA Alpha: 16
LoRA Dropout: 0.05
Task Type: Causal Language Modeling

Target Modules:
- q_proj
- k_proj
- v_proj
- o_proj
```

### Trainable Parameters

```text
Trainable parameters: 1,081,344
Total parameters:      495,114,112
Trainable percentage:  0.2184%
```

---

## Dataset

The project uses a Text-to-SQL dataset based on the Spider dataset.

### Dataset Size

```text
Total examples:       8,034
Training examples:    7,230
Validation examples:    804
```

### Dataset Columns

```text
text_query
sql_command
```

The dataset was transformed into a conversational format suitable for
instruction fine-tuning.

Example:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Convert the following question into SQL:\n\nWhat is the average salary?"
    },
    {
      "role": "assistant",
      "content": "SELECT AVG(salary) FROM employees;"
    }
  ]
}
```

---

## Project Structure

```text
SQLGenAI/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   │
│   │   ├── routes/
│   │   │   ├── sql.py
│   │   │   └── health.py
│   │   │
│   │   ├── schemas/
│   │   │   └── sql.py
│   │   │
│   │   ├── services/
│   │   │   ├── model_service.py
│   │   │   ├── sql_validator.py
│   │   │   └── sql_executor.py
│   │   │
│   │   └── database/
│   │       └── connection.py
│   │
│   └── requirements.txt
│
├── model/
│   ├── training/
│   │   ├── prepare_data.py
│   │   └── train.py
│   │
│   ├── inference/
│   │   └── generate_sql.py
│   │
│   └── evaluation/
│       └── evaluate.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── database/
│   └── schema.sql
│
├── tests/
│
├── .env
├── .env.example
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## How the System Works

### 1. User submits a question

Example:

```text
Show the top 5 employees with the highest salary.
```

### 2. FastAPI receives the request

The API receives:

```json
{
  "question": "Show the top 5 employees with the highest salary."
}
```

### 3. Fine-tuned model generates SQL

The question is passed to the fine-tuned Qwen2.5-Coder model.

Example generated SQL:

```sql
SELECT name FROM employees ORDER BY salary DESC LIMIT 5;
```

### 4. SQL validation

Before execution, the generated SQL is checked.

The system currently allows read-only `SELECT` queries and blocks
potentially destructive operations such as:

```text
INSERT
UPDATE
DELETE
DROP
ALTER
TRUNCATE
CREATE
```

### 5. PostgreSQL execution

The validated SQL query is executed against the PostgreSQL database.

### 6. Results are returned

The API returns the generated SQL and database results.

---

# PostgreSQL Database

The project currently uses a PostgreSQL database named:

```text
sqlgenai
```

The main table is:

```text
employees
```

### Employees Schema

| Column     | Type    |
| ---------- | ------- |
| id         | SERIAL  |
| name       | VARCHAR |
| department | VARCHAR |
| salary     | NUMERIC |

Example records:

```text
Rahul Sharma   IT          75000
Aman Verma     HR          55000
Priya Singh    IT          82000
Rohit Kumar    Finance     68000
Neha Gupta     Marketing   60000
Arjun Mehta    IT          95000
```

---

# API

## Base URL

When running locally:

```text
http://127.0.0.1:8000
```

---

## Swagger Documentation

FastAPI automatically provides interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Generate SQL

### Endpoint

```text
POST /sql/generate
```

### Request

```json
{
  "question": "Show the top 5 employees with the highest salary."
}
```

### Response

```json
{
  "question": "Show the top 5 employees with the highest salary.",
  "sql": "SELECT name FROM employees ORDER BY salary DESC LIMIT 5;",
  "results": [
    ["Arjun Mehta"],
    ["Karan Singh"],
    ["Priya Singh"],
    ["Rahul Sharma"],
    ["Vikas Yadav"]
  ]
}
```

---

# Example Queries

SQLGenAI can process questions such as:

```text
What is the average salary of all employees?

Which employees work in the IT department?

Who is the employee with the lowest salary?

How many employees work in the HR department?

Which employees earn more than 70000?

What is the highest salary among all employees?

Show all employees ordered by their salary from highest to lowest.

How many employees work in the Marketing department?

Who are the top three highest-paid employees?

What is the average salary of employees in the IT department?
```

---

# Local Setup

## 1. Clone the repository

```bash
git clone <your-repository-url>
cd SQLGenAI
```

## 2. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure environment variables

Create a `.env` file in the project root.

```env
DB_HOST=localhost
DB_NAME=sqlgenai
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432
```

Never commit `.env` to GitHub.

---

## 5. Create the database

Create a PostgreSQL database named:

```text
sqlgenai
```

Then execute:

```text
database/schema.sql
```

This creates the `employees` table and inserts sample data.

---

## 6. Run FastAPI

```bash
uvicorn backend.app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

# Docker

SQLGenAI is also containerized using Docker.

### Build the image

```bash
docker build -t sqlgenai .
```

### Run the container

```bash
docker run --env-file .env --add-host=host.docker.internal:host-gateway -p 8000:8000 sqlgenai
```

The API will then be available at:

```text
http://127.0.0.1:8000/docs
```

When running inside Docker, the application connects to PostgreSQL
running on the host machine through:

```text
host.docker.internal
```

---

# Security Considerations

Because SQL is generated dynamically by a language model, generated
queries should not be executed blindly.

SQLGenAI includes a validation layer that currently restricts execution
to read-only SQL operations.

The project also keeps database credentials in environment variables
rather than hard-coding them into the application.

---

# Development Workflow

The project follows this workflow:

```text
Dataset
   ↓
Data Preparation
   ↓
Base Model
   ↓
Fine-Tuning with LoRA
   ↓
Model Inference
   ↓
SQL Validation
   ↓
PostgreSQL
   ↓
FastAPI
   ↓
Docker
```

---

# Key Engineering Concepts Demonstrated

This project demonstrates practical experience with:

- Large Language Models
- Instruction fine-tuning
- Parameter-Efficient Fine-Tuning
- LoRA
- PEFT
- Hugging Face Transformers
- Natural Language Processing
- Text-to-SQL
- Prompt formatting
- Model inference
- SQL generation
- SQL validation
- PostgreSQL
- REST APIs
- FastAPI
- Docker
- Environment configuration

---

# Future Improvements

Possible future improvements include:

- More robust SQL validation
- Better SQL generation accuracy
- Automated evaluation metrics
- Support for multiple database schemas
- Database schema retrieval
- Query explanation
- Authentication and authorization
- Streaming responses
- Production deployment
- Monitoring and logging
- Web-based frontend

---

# Project Objective

The primary objective of SQLGenAI is to demonstrate how a fine-tuned
language model can be integrated into a real software system rather
than being used only for standalone text generation.

The project combines:

```text
LLM Fine-Tuning
        +
Backend Engineering
        +
Database Engineering
        +
API Development
        +
Containerization
```

to create an end-to-end Natural Language to SQL application.

---

## Author

**Shivam Kumar**

AI/ML Engineer | GenAI | LLMs | NLP | Python

````



```text
<https://github.com/kshivamr/SQLGenAI-Text-to-SQL-Converter.git>
````
