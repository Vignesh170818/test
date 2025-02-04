'''Base model for the input data'''
from pydantic import BaseModel, Field

class FunctionalDesignInput(BaseModel):
    '''Base model for the input data'''
    businesscontext: str = Field(default="")
    highlevelreq: str = Field(default="")
    applicationcontext: str = Field(default="")
    processflow: str = Field(default="")
    epic: str = Field(default="")
    feature: str = Field(default="")
    userstory: str = Field(default="")

class HighLevelDesignInput(BaseModel):
    '''Base model for the input data'''
    businesscontext: str = Field(default="")
    highlevelreq: str = Field(default="")
    applicationcontext: str = Field(default="")
    processflow: str = Field(default="")
    epic: str = Field(default="")
    feature: str = Field(default="")
    userstory: str = Field(default="")
    functionaldesign: str = Field(default="")

class LowLevelDesignInput(BaseModel):
    '''Base model for the input data'''
    businesscontext: str = Field(default="")
    highlevelreq: str = Field(default="")
    applicationcontext: str = Field(default="")
    processflow: str = Field(default="")
    epic: str = Field(default="")
    feature: str = Field(default="")
    userstory: str = Field(default="")
    functionaldesign: str = Field(default="")
    highleveldesign: str = Field(default="")
