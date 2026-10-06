from fastapi import APIRouter, Query, status

from userlife.infrastructure.db.models import Debt, Event, Idea, Note, Task
from userlife.presentation.api.dependencies import async_session, life_item_service
from userlife.application.dto.entities import (
    DebtCreate,
    DebtRead,
    EventCreate,
    EventRead,
    IdeaCreate,
    IdeaRead,
    NoteCreate,
    NoteRead,
    TaskCreate,
    TaskRead,
)


router = APIRouter(prefix="/api/v1")


@router.post("/notes", response_model=NoteRead, status_code=status.HTTP_201_CREATED)
async def create_note(payload: NoteCreate, session: async_session, service: life_item_service):
    return await service.create(session, Note, payload.model_dump())


@router.get("/notes", response_model=list[NoteRead])
async def list_notes(
    session: async_session,
    service: life_item_service,
    limit: int = Query(default=50, ge=1, le=100),
):
    return await service.list(session, Note, limit)


@router.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(payload: TaskCreate, session: async_session, service: life_item_service):
    return await service.create(session, Task, payload.model_dump())


@router.get("/tasks", response_model=list[TaskRead])
async def list_tasks(
    session: async_session,
    service: life_item_service,
    limit: int = Query(default=50, ge=1, le=100),
):
    return await service.list(session, Task, limit)


@router.post("/debts", response_model=DebtRead, status_code=status.HTTP_201_CREATED)
async def create_debt(payload: DebtCreate, session: async_session, service: life_item_service):
    return await service.create(session, Debt, payload.model_dump())


@router.get("/debts", response_model=list[DebtRead])
async def list_debts(
    session: async_session,
    service: life_item_service,
    limit: int = Query(default=50, ge=1, le=100),
):
    return await service.list(session, Debt, limit)


@router.post("/events", response_model=EventRead, status_code=status.HTTP_201_CREATED)
async def create_event(payload: EventCreate, session: async_session, service: life_item_service):
    return await service.create(session, Event, payload.model_dump())


@router.get("/events", response_model=list[EventRead])
async def list_events(
    session: async_session,
    service: life_item_service,
    limit: int = Query(default=50, ge=1, le=100),
):
    return await service.list(session, Event, limit)


@router.post("/ideas", response_model=IdeaRead, status_code=status.HTTP_201_CREATED)
async def create_idea(payload: IdeaCreate, session: async_session, service: life_item_service):
    return await service.create(session, Idea, payload.model_dump())


@router.get("/ideas", response_model=list[IdeaRead])
async def list_ideas(
    session: async_session,
    service: life_item_service,
    limit: int = Query(default=50, ge=1, le=100),
):
    return await service.list(session, Idea, limit)
