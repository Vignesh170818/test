'''This module contains the base model for the input data'''
from pydantic import BaseModel, Field

class GraphInput(BaseModel):
    '''Base model for the input data'''
    graphsourcecodelang: str = Field(default="")
    graphsourcecode: str = Field(default="")
    uniqueId: str = Field(default="")
