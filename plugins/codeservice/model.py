'''Base model for the input data'''
from pydantic import BaseModel

class CodeInput(BaseModel):
    '''Base model for the input data'''
    applicationcontext: str
    highleveldesign: str
    lowleveldesign: str
