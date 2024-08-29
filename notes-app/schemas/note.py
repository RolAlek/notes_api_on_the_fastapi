from pydantic import BaseModel, ConfigDict


class NoteCreate(BaseModel):
    name: str
    text: str


class NoteRead(NoteCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
