from typing import TypedDict, Literal, Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class Profile(BaseModel):
    """This is the profile of the user you are having conversation with"""
    name: Optional[str] = Field(description="The user's name", default=None)
    location: Optional[str] = Field(description="The user's location", default=None)
    team: Optional[str] = Field(description="The user's team", default="management")
    designation: Optional[str] = Field(description="The user's designation", default="manager")
    email: Optional[str] = Field(description="The user's email", default=None)


class TicketDetails(BaseModel):
    """This is the details of the ticket you created by analyzing user's input and conversations."""
    task: str = Field(description="The task to be completed.")
    time_to_complete: Optional[int] = Field(
        description="Estimated time to complete the task (minutes)."
    )
    deadline: Optional[datetime] = Field(
        description="When the task needs to be completed by (if applicable)",
        default=None
    )
    solutions: list[str] = Field(
        description="List of specific, actionable solutions (e.g., specific ideas, service providers, or concrete options relevant to completing the task)",
        min_items=1,
        default_factory=list
    )
    status: Literal["not started", "in progress", "done", "archived"] = Field(
        description="Current status of the task",
        default="not started"
    )


# Update memory tool
class UpdateMemory(TypedDict):
    """Decision on what memory type to update"""
    update_type: Literal['user', 'ticket', 'instructions', 'productresearch', 'userfeedback']
