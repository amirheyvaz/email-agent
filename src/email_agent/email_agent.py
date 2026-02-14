

from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool, ToolRuntime
from langchain.agents import create_agent
from langchain.agents.structured_output import ProviderStrategy
from loguru import logger
from typing import List
from langchain.agents import AgentState
import json
from langfuse.langchain import CallbackHandler
from .states import Category, AgentExpectedOutput

class EmailAgent():
    """Agent for processing incoming emails and generating appropriate responses based on the email content."""
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4.1-mini-2025-04-14", temperature=0.0)
        self.tools = [self.cash_application_tool, self.disputes_tool, self.ar_support_tool]
        self.langfuse_handler = CallbackHandler()
        self.agent = create_agent(
            model=self.llm,
            response_format=ProviderStrategy(AgentExpectedOutput),
            tools=self.tools,
            system_prompt=SystemMessage(
                content=(
                    "You are an assistant for categorizing and responding to emails. Also you should extract relevant customer information from the email. "
                    "Your task is to read the input email, categorize it into one of the following categories: "\
                    f"{Category.list_values()}, and then generate a response email based on the input email and the category. "
                    "Additionally, you should extract relevant customer information from the email, "
                    "including the customer's name, dates, amounts, invoice references, and dispute details if applicable. "
                    "Finally, you should call the appropriate tool based on the category of the email to process the email further. "
                    "If you could not categorize the email into any of the categories, you should categorize it as General AR Request and call the AR support tool. "
                    "Do not forget to call the tool. "
                )
            )
        )
        logger.info("Email agent initialized successfully.")
    
    async def aprocess_email(self, email: str) -> AgentExpectedOutput | None:
        """Process the incoming email and return the expected output."""
        logger.info("Processing incoming email.")
        response = await self.agent.ainvoke({
            "messages": [HumanMessage(content=email)]
        }#, config={"callbacks": [self.langfuse_handler]}
        )
        logger.info("Email processed successfully.")
        return response.get('structured_response')
    
    async def abatch_process_emails(self , emails: List[str]) -> List[AgentExpectedOutput | None]:
        """Process the incoming emails in batches and return the expected outputs."""
        logger.info("Processing incoming emails in batches.")
        responses = await self.agent.abatch(
            [
                {"messages": [HumanMessage(content=email)]} for email in emails
            ]#, config={"callbacks": [self.langfuse_handler]}
        )
        logger.info("Emails processed successfully.")
        return [
            response.get('structured_response') for response in responses
        ]

    @tool
    @staticmethod
    def cash_application_tool(runtime: ToolRuntime) -> None:
        """Tool for processing cash application related emails.
        This tool should be called if the category of the email is identified as Payment Claim.
        """
        logger.info("Processing email with cash application tool.")
        if runtime.state['messages'][-1].content:
            output = AgentExpectedOutput(**json.loads(runtime.state['messages'][-1].content))

    @tool
    @staticmethod
    def disputes_tool(runtime: ToolRuntime) -> None:
        """Tool for processing disputes related emails. 
        This tool should be called if the category of the email is identified as Dispute.
        """
        logger.info("Processing email with disputes tool.")
        if runtime.state['messages'][-1].content:
            output = AgentExpectedOutput(**json.loads(runtime.state['messages'][-1].content))

    @tool
    @staticmethod
    def ar_support_tool(runtime: ToolRuntime) -> None:
        """Tool for processing AR support related emails. 
        This tool should be called if the category of the email is identified as General AR Request.
        """
        logger.info("Processing email with AR support tool.")
        if runtime.state['messages'][-1].content:
            output = AgentExpectedOutput(**json.loads(runtime.state['messages'][-1].content))
