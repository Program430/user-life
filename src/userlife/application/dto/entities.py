from datetime import date, datetime
from decimal import Decimal
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)


class NoteRead(NoteCreate, ORMModel):
    id: UUID
    created_at: datetime
    updated_at: datetime


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    person: str | None = Field(default=None, max_length=200)
    due_at: datetime | None = None
    status: str = Field(default="open", max_length=30)
    priority: int = Field(default=0, ge=0, le=5)


class TaskRead(TaskCreate, ORMModel):
    id: UUID
    created_at: datetime
    updated_at: datetime


class DebtCreate(BaseModel):
    person: str = Field(min_length=1, max_length=200)
    amount: Decimal = Field(gt=0)
    currency: str = Field(min_length=3, max_length=3)
    direction: Literal["i_owe", "owed_to_me"]
    due_date: date | None = None
    status: str = Field(default="open", max_length=30)
    note: str | None = None


class DebtRead(DebtCreate, ORMModel):
    id: UUID
    created_at: datetime
    updated_at: datetime


class EventCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    starts_at: datetime
    ends_at: datetime | None = None
    location: str | None = Field(default=None, max_length=300)


class EventRead(EventCreate, ORMModel):
    id: UUID
    created_at: datetime
    updated_at: datetime


class IdeaCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)
    status: str = Field(default="active", max_length=30)


class IdeaRead(IdeaCreate, ORMModel):
    id: UUID
    created_at: datetime
    updated_at: datetime


ActionType = Literal["note", "task", "debt", "event", "idea"]


class AssistantAction(BaseModel):
    type: ActionType
    payload: dict[str, Any]


class AssistantAskRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10000)


class AssistantAskResponse(BaseModel):
    reply: str
    actions: list[AssistantAction] = Field(default_factory=list)
    provider: str
    model: str


class AssistantMessageRead(ORMModel):
    id: UUID
    role: str
    content: str
    provider: str | None
    model: str | None
    created_at: datetime
