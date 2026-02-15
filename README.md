# Transformance Email Agent

A LangChain-based agent that ingests AR-related customer emails, categorizes them (Payment Claim, Dispute, or General AR Request), generates structured responses, and extracts key customer information. The agent can process individual emails or batches and logs activity for observability.

## Features
- Categorization into Payment Claim, Dispute, or General AR Request via [`email_agent.states.Category`](src/email_agent/states.py).
- Structured outputs using [`email_agent.states.AgentExpectedOutput`](src/email_agent/states.py) with nested [`email_agent.states.EmailSchema`](src/email_agent/states.py) and [`email_agent.states.CustomerInformationSchema`](src/email_agent/states.py).
- LLM-powered workflow orchestrated by [`email_agent.EmailAgent`](src/email_agent/email_agent.py) using LangChain tools for cash application, disputes, and AR support.
- Batch processing example in [`src/main.py`](src/main.py).
- Sample dataset in [data/Sample Emails.json](data/Sample%20Emails.json).

## Prerequisites
- Python 3.13 (`.python-version` included)
- [uv](https://github.com/astral-sh/uv) package manager installed
- An OpenAI API key
- (Optional) Langfuse keys if you want tracing

## Setup (with uv)
1. Create and activate a virtual environment:
   ```bash
   uv venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   uv pip install --upgrade pip
   uv pip install -e .
   ```
3. Configure environment:
   ```bash
   cp .env.sample .env
   # then set OPENAI_API_KEY (and LANGFUSE_* if used)
   ```

## Running the agent
Execute the batch example (processes a slice of sample emails):
```bash
uv run python src/main.py
```
This will:
- Load environment variables
- Initialize logging to `logs/project.log`
- Process a subset of sample emails via [`email_agent.EmailAgent.abatch_process_emails`](src/email_agent/email_agent.py)

## Logging
- Log file: `logs/project.log` (rotated daily, 7-day retention, zipped)
- Controlled by `loguru` in [`src/main.py`](src/main.py) and [`email_agent.EmailAgent`](src/email_agent/email_agent.py)

## Langfuse (optional tracing)
- Set `LANGFUSE_SECRET_KEY`, `LANGFUSE_PUBLIC_KEY`, and `LANGFUSE_BASE_URL` in `.env`.
- With these set, Langfuse will capture traces from the agent runs for observability. Without them, tracing is skipped.

## Project structure
- `src/email_agent/` — core agent, schemas, categories
- `src/main.py` — batch execution example
- `data/Sample Emails.json` — synthetic input data
- `src/notebooks/` — notebooks and experiments