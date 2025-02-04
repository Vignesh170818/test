'''Base model for the input data'''
from pydantic import BaseModel

class BPMInput(BaseModel):
    '''Base model for the input data'''
    businesscontext: str
    highlevelreq: str
    applicationcontext: str
