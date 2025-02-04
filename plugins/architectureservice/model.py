'''This module contains the base model for the input data'''
from pydantic import BaseModel, Field

class ArchitectureInput(BaseModel):
    '''Base model for the input data'''
    applicationcontext: str = Field(default="")
    design: str = Field(default="")
    platform: str = Field(default="")
