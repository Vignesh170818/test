'''Input model for deployment service plugin'''

from pydantic import BaseModel, Field

class DeploymentInput(BaseModel):
    '''Base model for the input data'''

    design: str = Field(default="")
    architecture: str = Field(default="")
