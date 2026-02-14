

from typing import TypedDict, Annotated, List, Literal
from pydantic import BaseModel, Field
from enum import StrEnum

class EmailSchema(BaseModel):
    """Schema for representing an email message."""
    id: Annotated[str, Field(description="The unique identifier of the email")]
    receivedAt: Annotated[str, Field(description="The timestamp when the email was received")]
    sender: Annotated[str, Field(description="The sender of the email")]
    subject: Annotated[str, Field(description="The subject of the email")]
    body: Annotated[str, Field(description="The body content of the email")]
    reciever: Annotated[str, Field(description="The receiver of the email")]

class CustomerInformationSchema(BaseModel):
    """Schema for extracting customer information from the email."""
    name: Annotated[str, Field(description="The name of the customer.")]
    dates: Annotated[List[str], Field(
        description="The dates referenced in the email by the customer, in the format YYYY-MM-DD."
        )]
    amounts: Annotated[List[str], Field(
        description="The amounts referenced in the email by the customer."
        )]
    invoice_references: Annotated[List[str], Field(
        description="The list of invoice IDs referenced in the email by the customer." \
        "")]
    dispute_details: Annotated[str, Field(
        description="The details of the dispute as described by the customer in the email."
        )]

class Category(StrEnum):
    """Enum for categorizing the email into one of the categories."""
    PAYMENT_CLAIM = "Payment Claim"
    DISPUTE = "Dispute"
    GENERAL_AR_REQUEST = "General AR Request"

    @classmethod
    def list_values(cls) -> str:
        """Helper method to list the values of the enum members as a comma-separated string."""
        return ", ".join([c.value for c in cls]).rstrip()

class AgentExpectedOutput(BaseModel):
    """Schema for representing the expected output of the agent.
    First the agent is expected to categorize the email.
    Then, the agent is expected to generate a response email based on the input email and the category,
    and also extract the customer information from the email.
    """
    response_email: Annotated[EmailSchema, Field(description=(
        "The response email that the agent should generate based on the input email and the category. "
        "Our company's email address is: info@transformance.com. "
        f"if the category is {Category.PAYMENT_CLAIM.value}, "
        "the response email should include a payment claim response. "
        f"if the category is {Category.DISPUTE.value}, the response email "
        "should include a dispute response. "
        f"if the category is {Category.GENERAL_AR_REQUEST.value}, "
        "the response email should include a general AR request response."
    ))]
    category: Annotated[Category, Field(
        description=f"The category of the email, which can be one of the following: {Category.list_values()}."
        )]
    customer_information: Annotated[CustomerInformationSchema, Field(
        description=(
            "The extracted customer information from the email, which includes "
            "the customer's name, dates, amounts, invoice references, "
            "and dispute details if applicable."
        )
    )]
