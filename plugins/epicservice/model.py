'''Base model for the input data'''
from pydantic import BaseModel, Field

class EPICInput(BaseModel):
    '''Base model for the input data'''
    businesscontext: str = Field(default="")
    highlevelreq: str = Field(default="")
    applicationcontext: str = Field(default="")
    processflow: str = Field(default="")

class EPICReviewInput(BaseModel):
    '''Base model for the input data'''
    businesscontext: str = Field(default="")
    highlevelreq: str = Field(default="")
    applicationcontext: str = Field(default="")
    processflow: str = Field(default="")
    reviewpersona: str = Field(default="")
    epic: str = Field(default="")

class EPICApplyReviewInput(BaseModel):
    '''Base model for the input data'''
    businesscontext: str = Field(default="")
    highlevelreq: str = Field(default="")
    applicationcontext: str = Field(default="")
    processflow: str = Field(default="")
    epic: str = Field(default="")
    reviewcomments: str = Field(default="")
