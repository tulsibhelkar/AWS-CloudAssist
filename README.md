# AWS CloudAssist
### A Domain-Specific RAG Assistant for AWS Technical Support

AWS CloudAssist is a documentation-grounded AI assistant designed to answer technical questions about Amazon EC2, Amazon S3, and AWS Identity and Access Management (IAM).

The application uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from collected AWS documentation and generate answers using a locally hosted language model. It provides source links so users can refer to the original documentation.

> **Disclaimer:** AWS CloudAssist is an independent student project and is not affiliated with or endorsed by Amazon Web Services. Answers should be verified against current AWS documentation before making production or security-related decisions.

---

## 1. Project Overview

AWS technical documentation contains extensive information across multiple services. Finding a specific answer may require navigating several pages.

AWS CloudAssist provides a conversational interface that allows users to ask questions and receive responses based on a focused AWS documentation knowledge base.

### Supported Services

- **Amazon EC2:** Cloud computing, instances, instance types, and related concepts.
- **Amazon S3:** Object storage, buckets, and related storage concepts.
- **AWS IAM:** Identity management, authentication, and authorization.

The assistant's coverage is limited to the documentation currently included in its knowledge base.

---

## 2. Key Features

- Documentation-based question answering using RAG.
- Automated collection of selected AWS documentation pages.
- Data cleaning and text chunking.
- Semantic search using sentence embeddings.
- Persistent vector storage with ChromaDB.
- Local answer generation using Ollama and Llama 3.2.
- Streamlit-based conversational interface.
- Chat history within the current Streamlit session.
- AWS documentation source links.
- Response-time tracking.
- Refusal handling for questions unsupported by the retrieved documentation.

**Note:** Refusal handling and citation accuracy are still being evaluated. Retrieved source links do not guarantee that every generated statement is supported.

---

## 3. Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python 3.12 |
| Frontend | Streamlit |
| Data collection | Requests, Beautiful Soup |
| Data processing | Python, JSON |
| Text chunking | LangChain Text Splitters |
| Embedding model | all-MiniLM-L6-v2 |
| Vector database | ChromaDB |
| Language model | Llama 3.2 3B |
| Local model runtime | Ollama |
| Development environment | Visual Studio Code |

---

## 4. System Architecture

```text
              AWS Documentation
                      |
                      v
              Data Collection
               collect_data.py
                      |
                      v
                 Raw JSON
                      |
                      v
                Data Cleaning
                clean_data.py
                      |
                      v
                Text Chunking
                chunk_data.py
                      |
                      v
              Sentence Embeddings
             create_embeddings.py
                      |
                      v
                  ChromaDB
                      |
                      |
User Question --------+
                      |
                      v
              Semantic Retrieval
                 retrieve.py
                      |
                      v
             Retrieved AWS Context
                      |
                      v
              Ollama + Llama 3.2
              generate_answer.py
                      |
                      v
           Answer + Documentation Links
                      |
                      v
               Streamlit Interface
                    app.py
```

---

## 5. Project Structure

```text
AWS-CloudAssist/
|
|-- app.py
|-- README.md
|-- requirements.txt
|
|-- data/
|   |-- raw/
|   |   |-- ec2_001.json
|   |   |-- s3_001.json
|   |   |-- iam_001.json
|   |
|   |-- processed/
|   |   |-- ec2_001.json
|   |   |-- s3_001.json
|   |   |-- iam_001.json
|   |   |-- chunks.json
|   |
|   |-- chroma_db/
|
|-- src/
|   |-- collect_data.py
|   |-- clean_data.py
|   |-- chunk_data.py
|   |-- create_embeddings.py
|   |-- retrieve.py
|   |-- generate_answer.py
|
|-- evaluation/
|
|-- .venv/
```

The `evaluation/` directory is reserved for upcoming evaluation scripts and results.

The `.venv/` directory and local vector database should generally not be committed to Git.

---

## 6. Dataset Preparation

The initial knowledge base contains three selected official AWS documentation pages:

1. Amazon EC2 overview.
2. Amazon S3 overview.
3. AWS IAM introduction.

The collection script checks `robots.txt` before requesting documentation pages and skips pages when crawling permission cannot be verified.

### Data Processing Pipeline

**Step 1 — Collection**

The collector extracts documentation text and stores it in JSON format with metadata such as:

- Document ID
- AWS service
- Document title
- Source URL
- Collection timestamp
- Document content

**Step 2 — Cleaning**

The cleaning script normalizes whitespace while preserving line boundaries and source metadata.

**Step 3 — Chunking**

Documents are divided into smaller text segments using a recursive character splitter.

Configuration:

```python
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
```

The current dataset contains **62 text chunks**.

**Step 4 — Embeddings**

The `all-MiniLM-L6-v2` model converts the text chunks into 384-dimensional embeddings.

**Step 5 — Vector Storage**

ChromaDB stores the embeddings, text, chunk IDs, and document metadata for semantic retrieval.

---

## 7. Installation and Setup

### Prerequisites

- Python 3.12
- Git
- Ollama
- Internet connection for initial dependency and model downloads

### Step 1: Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd AWS-CloudAssist
```

Replace `<YOUR_REPOSITORY_URL>` with the actual GitHub repository URL after publishing the project.

### Step 2: Create a Virtual Environment

On Windows CMD:

```cmd
py -3.12 -m venv .venv
.venv\Scripts\activate.bat
```

### Step 3: Install Dependencies

```cmd
python -m pip install -r requirements.txt
```

Ensure `requirements.txt` contains the packages required by the project, including Streamlit, Requests, Beautiful Soup, lxml, LangChain Text Splitters, Sentence Transformers, and ChromaDB.

### Step 4: Install Ollama

Download Ollama from:

https://ollama.com/download

Pull the language model:

```cmd
ollama pull llama3.2:3b
```

Make sure the Ollama service is running before using the chatbot.

### Step 5: Prepare the Knowledge Base

Run the following scripts in order:

```cmd
python src\collect_data.py
python src\clean_data.py
python src\chunk_data.py
python src\create_embeddings.py
```

The collection step requires internet access. Review the collected documents before proceeding to embeddings.

**Warning:** The current embedding script replaces the existing ChromaDB collection named `aws_cloudassist` when it runs.

### Step 6: Test Retrieval

```cmd
python src\retrieve.py
```

Example question:

```text
What is an EC2 instance?
```

### Step 7: Run the Command-Line Chatbot

```cmd
python src\generate_answer.py
```

Type `exit` or `quit` to close the chatbot.

### Step 8: Launch the Web Application

```cmd
python -m streamlit run app.py
```

Open the local address displayed by Streamlit, typically:

http://localhost:8501

---

## 8. Example Questions

AWS CloudAssist can be tested with questions such as:

```text
What is an EC2 instance?

What is Amazon S3?

What is AWS IAM?

What are the features of Amazon EC2?
```

The ability to answer a question depends on whether the required information is present in the collected documentation.

### Example Answer

**Question:**

What is an EC2 instance?

**Answer:**

An EC2 instance is a virtual server in the AWS Cloud. The instance type determines the hardware resources available to the instance.

**Source:**

https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html

This example is based on a successful local test.

---

## 9. Testing and Current Results

The following development checks have been completed:

| Test | Observed result |
|---|---|
| Documentation collection | 3 documents collected |
| Text chunking | 62 chunks created |
| Embedding generation | 62 embeddings generated |
| Vector storage | 62 chunks stored in ChromaDB |
| EC2 retrieval | Relevant EC2 documentation retrieved |
| EC2 answer generation | Relevant answer generated with source link |
| Unsupported weather question | Assistant returned a refusal |

The unsupported-question test also revealed an issue with irrelevant source links. The answer-generation code was subsequently updated to suppress source links when the model returns its predefined refusal message.

**Formal evaluation has not yet been completed.** Accuracy, retrieval precision, hallucination rate, latency, and user satisfaction should not be reported as achieved metrics until measured.

---

## 10. Current Limitations

- The knowledge base initially contains only three AWS documentation pages.
- The assistant does not cover all AWS services or every EC2, S3, and IAM topic.
- Responses may be slower on systems running the language model on a CPU.
- The assistant cannot inspect or modify a user's live AWS account.
- The current refusal mechanism does not guarantee detection of every unsupported question.
- Source links identify retrieved documents but do not independently verify every generated statement.
- The application currently runs locally and has not been deployed publicly.

---

## 11. Future Enhancements

- Expand the knowledge base with additional official AWS documentation.
- Add service-specific retrieval filters.
- Introduce relevance thresholds for unsupported questions.
- Improve chunking to preserve technical headings and code blocks.
- Implement retrieval and answer-quality evaluation.
- Improve citation accuracy.
- Optimize model loading and response latency.
- Add automated tests and deployment configuration.

---

## 12. Author

**Tulsi Bhelkar**

B.Tech — Computer Science and Engineering (Data Science)

St. Vincent Pallotti College of Engineering and Technology, Nagpur

---

## 13. Acknowledgments

This project uses official AWS documentation as its knowledge source and open-source tools for document processing, retrieval, language-model inference, and the user interface.

AWS and related service names are trademarks of Amazon.com, Inc. or its affiliates.

---

**AWS CloudAssist — Making selected AWS documentation accessible through conversational AI.**