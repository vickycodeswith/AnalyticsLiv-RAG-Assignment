# Design Note — NovaTech Knowledge Assistant

## Goal and data
This project demonstrates question answering over a fictional company's documents and relational records. The sample SQLite database contains 60 projects, 100 employees, and 150 support tickets. Foreign keys connect employees to projects and tickets to employees. Six documents are supplied in PDF, DOCX, and TXT formats. The sample data is fictional and was created for this assignment.

## Chunking and embeddings
Documents are split into chunks of about 700 characters with roughly 120 characters of overlap. The chunk size aims to preserve a useful policy or procedure passage without sending an entire document to the model; overlap helps retain context near boundaries. The local `all-MiniLM-L6-v2` Sentence Transformers model creates normalized embeddings. ChromaDB stores the vectors, text, and source metadata. The model is small enough for a student project, but a larger domain-specific model may improve retrieval quality.

## Retrieval and generation
The application embeds the user's question and runs top-k cosine similarity search. Each result retains its file/page or table/record metadata and is shown in the interface. A configurable distance threshold is used as a simple relevance filter; it must be tuned against the evaluation set and is not a guarantee of correctness. Gemini receives only retrieved evidence and is instructed to answer from that evidence, cite sources, and say when the information is missing. Document text is treated as untrusted reference material, not as instructions.

Database questions use a Gemini-generated read-only SQLite SELECT query when possible. The query is checked for disallowed operations and executed against a read-only database connection. This can answer aggregations (for example, counting open tickets) more reliably than trying to count a few retrieved row embeddings. The SQL route is still a limitation: generated SQL may be invalid or may misunderstand an ambiguous question. A production implementation should use a stricter SQL parser, allowlisted query templates, and additional tests.

## Trade-offs and known limitations
- DOCX and TXT ingestion currently records the file name but not exact page numbers; PDF pages are tracked individually.
- Vector distance thresholds can reject valid evidence or admit weak matches. They should be tuned with the evaluation sheet.
- A local embedding model requires a first-run download and consumes memory.
- The demo uses a fictional dataset and a single local Chroma collection; it is not intended for multi-user production workloads.
- Gemini API use requires a valid API key and may incur usage charges.

## Improvements with more time
Add hybrid keyword/vector retrieval or reranking, evaluate retrieval recall at k, use an AST-based SQL validator and query allowlist, add automated regression tests for all evaluation questions, and implement document re-indexing when files change. For around 100,000 documents, use batched ingestion, a managed vector database, asynchronous indexing, metadata filters, monitoring, and a reranking stage.

## Evaluation status
The repository includes 18 questions covering lookups, multi-source reasoning, and unanswerable questions. Actual answers, retrieval correctness, and correctness labels must be filled after running each question against the deployed application. No evaluation scores are claimed before those runs.
