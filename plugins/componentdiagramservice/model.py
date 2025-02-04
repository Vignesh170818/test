'''Input model for the component diagram service'''
from pydantic import BaseModel, Field

class ComponentDiagramInput(BaseModel):
    '''Base model for the input data'''

    applicationcontext: str = Field(default="")
    design: str = Field(default="")
    architecture: str = Field(default="")  
