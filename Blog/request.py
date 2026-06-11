from pydantic import BaseModel

class PostCreateRequest(BaseModel):
    title: str
    content: str | None = None


class PostUpdateRequest(BaseModel):   
    title: str | None = None
    content: str | None = None