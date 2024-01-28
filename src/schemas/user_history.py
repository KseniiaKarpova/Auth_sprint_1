from pydantic import BaseModel, Field

class UserHistory(BaseModel):
    user_agent: str = Field(description="The device user logined from")

    class Config:
        from_attributes = True
