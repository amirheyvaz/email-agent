from loguru import logger
import json
from email_agent import EmailAgent, AgentExpectedOutput
import asyncio
from dotenv import load_dotenv
from typing import List

def init_logger():
    """Initialize the logger for the project."""
    logger.add("logs/project.log", format="{time} - {level} - {message}", 
               rotation="1 day", retention="7 days", compression="zip", level="INFO")

def read_emails() -> list[str]:
    with open("data/Sample Emails.json", "r") as f:
        email_data = json.load(f).get("emails", [])
    return [json.dumps(email) for email in email_data]

async def main() -> None:
    _ = load_dotenv()
    init_logger()
    emails = read_emails()
    sample_emails = emails[:5]
    email_agent = EmailAgent()
    results: List[AgentExpectedOutput | None] = await email_agent.abatch_process_emails(sample_emails)

if __name__ == "__main__":
    asyncio.run(main())