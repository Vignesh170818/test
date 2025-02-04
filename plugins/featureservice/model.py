'''Base model for the input data'''
from pydantic import BaseModel, Field

class FeatureInput(BaseModel):
    '''Base model for the input data'''
    industry: str = Field(default="")
    businesscontext: str = Field(default="")
    highlevelreq: str = Field(default="")
    applicationcontext: str = Field(default="")
    processflow: str = Field(default="")
    epic: str = Field(default="")

class ExpandFeatureInput(BaseModel):
    '''Base model for the input data'''
    industry: str = Field(default="")
    businesscontext: str = Field(default="")
    highlevelreq: str = Field(default="")
    applicationcontext: str = Field(default="")
    processflow: str = Field(default="")
    epic: str = Field(default="")
    feature: str = Field(default="")
