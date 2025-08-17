"""
models/dummy_model.py: Defines the Dummy data model (schema reference)
"""


# Pydantic model for strict validation
from pydantic import BaseModel, Field

class DummyModel(BaseModel):
    name: str = Field(..., min_length=1)
    age: int = Field(..., ge=0)
