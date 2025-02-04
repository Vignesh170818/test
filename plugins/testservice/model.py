'''Base model for the input data'''
from pydantic import BaseModel, Field

class TestScenariosInput(BaseModel):
    '''Base model for the input data'''
    businesscontext: str = Field(default="")
    highlevelreq: str = Field(default="")
    applicationcontext: str = Field(default="")
    processflow: str = Field(default="")
    epic: str = Field(default="")
    feature: str = Field(default="")
    userstory: str = Field(default="")
    functionaldesignui: str = Field(default="")
    functionaldesignservices: str = Field(default="")
    functionaldesigndata: str = Field(default="")

class TestCasesInput(BaseModel):
    '''Base model for the input data'''
    businesscontext: str = Field(default="")
    highlevelreq: str = Field(default="")
    applicationcontext: str = Field(default="")
    processflow: str = Field(default="")
    epic: str = Field(default="")
    feature: str = Field(default="")
    userstory: str = Field(default="")
    functionaldesignui: str = Field(default="")
    functionaldesignservices: str = Field(default="")
    functionaldesigndata: str = Field(default="")
    testscenario: str = Field(default="")

class TestScriptsInput(BaseModel):
    '''Base model for the input data'''
    businesscontext: str = Field(default="")
    highlevelreq: str = Field(default="")
    applicationcontext: str = Field(default="")
    processflow: str = Field(default="")
    epic: str = Field(default="")
    feature: str = Field(default="")
    userstory: str = Field(default="")
    functionaldesignui: str = Field(default="")
    functionaldesignservices: str = Field(default="")
    functionaldesigndata: str = Field(default="")
    testscenario: str = Field(default="")
    testcase: str = Field(default="")

class ToolTestScriptsInput(BaseModel):
    '''Base model for the input data'''
    businesscontext: str = Field(default="")
    highlevelreq: str = Field(default="")
    applicationcontext: str = Field(default="")
    processflow: str = Field(default="")
    epic: str = Field(default="")
    feature: str = Field(default="")
    userstory: str = Field(default="")
    functionaldesignui: str = Field(default="")
    functionaldesignservices: str = Field(default="")
    functionaldesigndata: str = Field(default="")
    testscenario: str = Field(default="")
    testcase: str = Field(default="")
    testscript: str = Field(default="")
    tool: str = Field(default="")
