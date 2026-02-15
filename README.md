# Email Agent

An intelligent email processing agent built with LangChain and OpenAI that automatically categorizes, processes, and responds to incoming emails related to accounts receivable (AR) operations.

## Overview

Email Agent is an AI-powered system designed to streamline email management for AR departments. It uses advanced language models to:
- Automatically categorize incoming emails into predefined categories
- Extract relevant customer information (names, dates, amounts, invoice references, dispute details)
- Generate appropriate response emails based on email content and category
- Route emails to specialized processing tools based on their category
- Process emails both individually and in batches for efficiency

## Features

- **Intelligent Email Categorization**: Automatically categorizes emails into:
  - Payment Claim
  - Dispute
  - General AR Request

- **Customer Information Extraction**: Extracts key information including:
  - Customer name/company name
  - Referenced dates
  - Payment amounts
  - Invoice references
  - Dispute details

- **Automated Response Generation**: Creates contextually appropriate response emails based on the email category and content

- **Tool-Based Processing**: Routes categorized emails to specialized tools:
  - Cash Application Tool (for Payment Claims)
  - Disputes Tool (for Disputes)
  - AR Support Tool (for General AR Requests)

- **Batch Processing**: Efficiently processes multiple emails simultaneously using async operations

- **Observability**: Integrated with Langfuse for monitoring and tracing agent interactions

- **Structured Logging**: Uses Loguru for comprehensive logging with rotation and compression

## Installation

### Prerequisites

- Python 3.13 or higher
- OpenAI API key
- (Optional) Langfuse account for observability

### Setup

1. Clone the repository:
```bash
git clone https://github.com/amirheyvaz/email-agent.git
cd email-agent
```

2. Install dependencies using `uv` (recommended) or `pip`:

Using uv:
```bash
pip install uv
uv sync
```

Using pip:
```bash
pip install -e .
```

3. Create a `.env` file based on `.env.sample`:
```bash
cp .env.sample .env
```

4. Configure your environment variables in `.env`:
```env
OPENAI_API_KEY=your_openai_api_key_here
LANGFUSE_SECRET_KEY=your_langfuse_secret_key (optional)
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key (optional)
LANGFUSE_BASE_URL=https://cloud.langfuse.com (optional)
```

## Usage

### Basic Usage

Run the main script to process sample emails:

```bash
python src/main.py
```

The script will:
1. Load sample emails from `data/Sample Emails.json`
2. Process a subset of emails (emails 10-15 by default)
3. Generate categorized responses and extract customer information
4. Log results to `logs/project.log`

### Processing Individual Emails

```python
from email_agent import EmailAgent
import asyncio

async def process_single_email():
    email_agent = EmailAgent()
    
    email = """
    {
        "id": "email_001",
        "receivedAt": "2026-01-20T08:00:00Z",
        "from": "customer@example.com",
        "subject": "Payment sent - Invoice #12345",
        "body": "We have sent payment for invoice #12345 via ACH today."
    }
    """
    
    result = await email_agent.aprocess_email(email)
    print(result)

asyncio.run(process_single_email())
```

### Batch Processing

```python
from email_agent import EmailAgent
import asyncio
from typing import List

async def process_multiple_emails():
    email_agent = EmailAgent()
    
    emails: List[str] = [
        # List of JSON-serialized email strings
        email1,
        email2,
        email3
    ]
    
    results = await email_agent.abatch_process_emails(emails)
    for result in results:
        print(f"Category: {result.category}")
        print(f"Response: {result.response_email}")
        print(f"Customer Info: {result.customer_information}")
        print("---")

asyncio.run(process_multiple_emails())
```

## Project Structure

```
email-agent/
├── src/
│   ├── main.py                 # Main entry point for the application
│   └── email_agent/
│       ├── __init__.py         # Package initialization
│       ├── email_agent.py      # Core EmailAgent class implementation
│       └── states.py           # Pydantic models and state definitions
├── data/
│   └── Sample Emails.json      # Sample email data for testing
├── logs/                       # Application logs (auto-generated)
├── .env.sample                 # Environment variable template
├── .gitignore                  # Git ignore configuration
├── .python-version             # Python version specification
├── pyproject.toml              # Project dependencies and metadata
├── uv.lock                     # Locked dependency versions
└── README.md                   # This file
```

## API Documentation

### EmailAgent Class

The main class for processing emails.

#### Methods

**`__init__()`**
- Initializes the EmailAgent with GPT-4.1-mini model and specialized tools
- Sets up Langfuse callback handler for observability

**`aprocess_email(email: str) -> AgentExpectedOutput | None`**
- Processes a single email asynchronously
- Parameters:
  - `email`: JSON string containing email data
- Returns: `AgentExpectedOutput` object with categorization, response, and extracted information

**`abatch_process_emails(emails: List[str]) -> List[AgentExpectedOutput | None]`**
- Processes multiple emails in batch asynchronously
- Parameters:
  - `emails`: List of JSON strings containing email data
- Returns: List of `AgentExpectedOutput` objects

### Data Models

**`EmailSchema`**
- `id`: Unique identifier
- `receivedAt`: Timestamp
- `sender`: Email sender
- `subject`: Email subject
- `body`: Email content
- `receiver`: Email receiver

**`CustomerInformationSchema`**
- `name`: Customer/company name
- `dates`: Referenced dates (YYYY-MM-DD format)
- `amounts`: Referenced payment amounts
- `invoice_references`: Invoice IDs
- `dispute_details`: Dispute information

**`Category`** (Enum)
- `PAYMENT_CLAIM`: "Payment Claim"
- `DISPUTE`: "Dispute"
- `GENERAL_AR_REQUEST`: "General AR Request"

**`AgentExpectedOutput`**
- `response_email`: Generated response email (EmailSchema)
- `category`: Email category (Category enum)
- `customer_information`: Extracted customer data (CustomerInformationSchema)

## Tools

The agent uses three specialized tools for processing different email categories:

1. **Cash Application Tool**: Handles payment-related emails
2. **Disputes Tool**: Manages dispute communications
3. **AR Support Tool**: Processes general AR requests

## Logging

Logs are automatically saved to `logs/project.log` with:
- Daily rotation
- 7-day retention
- Automatic compression (zip)
- INFO level and above

## Dependencies

Core dependencies:
- `langchain` - LLM orchestration framework
- `langchain-openai` - OpenAI integration
- `langgraph` - Agent workflow management
- `openai` - OpenAI API client
- `langfuse` - LLM observability
- `loguru` - Advanced logging
- `python-dotenv` - Environment variable management
- `pydantic` - Data validation

See `pyproject.toml` for complete dependency list.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the terms specified in the repository.

## Company Information

Response emails are sent from: **info@transformance.com**

## Support

For issues, questions, or contributions, please open an issue on the GitHub repository.