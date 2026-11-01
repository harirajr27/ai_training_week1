
from pydantic import BaseModel, EmailStr, Field


class EmployeeBase(BaseModel):
    name: str = Field(..., min_length=1, description="Name cannot be empty")
    email: EmailStr
    department: str | None = None
    salary: float = Field(..., gt=0, description="Salary must be greater than 0")


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    name: str | None = Field(None, min_length=1)
    email: EmailStr | None = None
    department: str | None = None
    salary: float | None = Field(None, gt=0)


class EmployeeResponse(EmployeeBase):
    id: int

    class Config:
        from_attributes = True
