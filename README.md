# Saudi Legal Classification and Retrieval

Graduation project: classify an Arabic legal complaint and retrieve relevant
articles from the Saudi Civil Transactions Law, Evidence Law, and Commercial
Courts Law. The pipeline uses Claude for law selection, hierarchical
classification, hypothetical query generation (HyDE), and article reranking;
multilingual E5 embeddings and Chroma provide semantic retrieval.

## Required files

| File | Purpose |
| --- | --- |
| `main.py` | Classification prompts and retrieval pipeline, with a command-line entry point |
| `data.py` | Build the local vector database |
| `data/legal_articles.json` | 946 legal articles and their existing classification metadata |
| `requirements.txt` | Python dependencies |
| `.env.example` | Configuration template without credentials |

The dataset was exported from the project's existing `Saudi_law` collection.
It preserves article text, IDs, and metadata; it contains no embeddings or
commercial case records. It is a project dataset, not a newly verified legal
edition.

## Setup and run

Use Python 3.12. From the repository directory, on Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and set your own `ANTHROPIC_API_KEY`. Then:

```powershell
.\.venv\Scripts\python.exe data.py
.\.venv\Scripts\python.exe main.py "اشتريت سيارة ووجدت فيها عيباً وأريد فسخ البيع"
```

On macOS/Linux, use `python3.12 -m venv .venv`, `.venv/bin/python` in place of
the Windows Python path, and `cp .env.example .env`.

The index builder downloads `intfloat/multilingual-e5-large` on its first run.
Indexing requires internet access and sufficient memory for that model.
Running a complaint makes paid Anthropic API calls using
`claude-haiku-4-5-20251001`. The model must be available to your API account.
`LEGAL_DB_PATH` optionally selects a different index directory; both scripts
use the same setting. The index can be rebuilt from the included JSON.

The program prints retrieved articles and returns pipeline details through
`run_full_pipeline_v2(query)`. Each run writes a local log under `logs/`.
Legal advice generation is disabled in this entry point, matching the original
pipeline. The final article list consists of the top reranked retrieval results
for each selected law.

## Submission scope

This is the application-only submission. Evaluation experiments, benchmark
scripts/results, spreadsheets, development tools, caches, logs, API test scripts,
and the original Git history are excluded. This copy changes configuration and
the command-line example to make it portable; it keeps the application prompts
and retrieval logic. Explicit temperature settings are omitted to use provider
defaults, consistent with the existing retrieval study compatibility notes.
This submission does not reproduce that separate study.

Validation before submission checked Python syntax, dataset completeness,
offline pipeline initialization, and database-builder inputs. A full live query
and a fresh embedding build were not run as part of packaging.
