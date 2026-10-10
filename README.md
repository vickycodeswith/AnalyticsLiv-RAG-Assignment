# NovaTech Knowledge Assistant

A student-sized Retrieval-Augmented Generation (RAG) demo for the AnalyticsLiv Data Science Intern assignment. It answers questions using a fictional business database and a small set of business documents, and displays evidence used for each answer.


Live app: https://analyticsliv-rag-assignment.streamlit.app/

## Features

- Ingests PDF, DOCX, and TXT files.
- Splits documents into overlapping chunks and records source metadata.
- Creates local embeddings with Sentence Transformers and stores them in ChromaDB.
- Converts SQLite rows into searchable records.
- Uses a read-only, validated SQL path for database questions, including simple aggregates.
- Uses Gemini to write answers grounded in retrieved evidence.
- Displays source chunks and database query details.
- Includes an 18-question evaluation sheet and a one-page design note.

## Sample data

All sample data is fictional. The database includes:

- `projects`: 60 rows
- `employees`: 100 rows
- `support_tickets`: 150 rows

Foreign keys connect `employees.project_id` to `projects.project_id` and `support_tickets.employee_id` to `employees.employee_id`.

The `data/documents/` folder contains six business documents in PDF, DOCX, and TXT formats. `data/schema.sql` contains the schema; `data/novatech_dump.sql` is a SQL dump; `data/novatech.db` is a ready-to-use database file.

## Setup (macOS / Linux)

Python 3.11 or 3.12 is recommended for the smoothest compatibility with the ML dependencies.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

Open `.env` and set `GEMINI_API_KEY` to your own key. Never commit `.env` or paste the key into source code.

## Run locally

```bash
streamlit run app.py
```

In the sidebar, click **Build / refresh index**. The first run downloads the embedding model and creates the local Chroma index. Then ask questions in the interface. The index is stored in `.chroma/` and can be rebuilt from the source documents and database at any time.

## Streamlit Community Cloud deployment

1. Push this project to a GitHub repository without `.env` or `.chroma/`.
2. Create a Streamlit Community Cloud app and select `app.py` as the main file.
3. In the app's **Settings → Secrets**, add:

```toml
GEMINI_API_KEY = "your-key-here"
GEMINI_MODEL = "gemini-2.5-flash"
```

4. Deploy, open the public URL, click **Build / refresh index**, and test the required cases.

The app writes a local Chroma index at runtime. Hosted filesystem persistence may not be permanent, so rebuild the index after a restart if needed. For a small demo this is acceptable; production hosting should use persistent storage or a managed vector database.

## Architecture

1. **Ingestion:** PyMuPDF reads PDFs, `python-docx` reads DOCX, and Python reads TXT.
2. **Chunking:** approximately 700 characters per chunk with 120-character overlap.
3. **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2` with normalized vectors.
4. **Vector retrieval:** ChromaDB cosine similarity, top-k search, and a configurable distance threshold.
5. **Structured data:** database rows are indexed as text; a separate read-only SQL path supports questions that need filters or aggregates.
6. **Generation:** Gemini answers from retrieved evidence and is instructed to decline when evidence is insufficient.
7. **Sources:** each chunk carries its source file/page or table/record metadata.

## Evaluation

Open `evaluation_sheet.csv`. Run all 18 questions against the application and fill `Actual answer`, `Right chunk retrieved?`, `Correct?`, and `Notes / failure analysis`. Use `Yes`, `Partly`, or `No` consistently. Do not report scores until you have run the tests.

Required behaviours to verify:

- A question answered from one document.
- A question requiring multiple chunks/documents.
- A database question, including a count/aggregate.
- An out-of-scope question that is declined without fabrication.
- Visible sources for every answer.

## Limitations and assumptions

- This is a fictional dataset and a learning/demo application, not a production system.
- Exact page metadata is available for PDF pages; DOCX/TXT sources use file-level metadata.
- Similarity thresholds are heuristics and need evaluation-based tuning.
- Gemini calls require an API key and may incur charges.
- The generated SQL path rejects many unsafe operations but should be hardened with a SQL parser and allowlisted query templates before production use.

See `design_note.md` for the design rationale and improvement plan.
