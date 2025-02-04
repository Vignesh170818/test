'''Main module for the FastAPI application'''
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from plugins.designservice.controller import GenLiteDesign
from plugins.designservice.model import (
    FunctionalDesignInput,
    HighLevelDesignInput,
    LowLevelDesignInput
    )

app = FastAPI()
cors = CORSMiddleware(
    app,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
    )
app.add_middleware(cors)

@app.post("/generatefunctionaldesign")
def generate_functional_design(functionaldesigninputdata: FunctionalDesignInput):
    '''Generate a functional design for given business context'''
    functionaldesign = GenLiteDesign(
        industry="healthcare"
        ).generate_functional_design(
            functionaldesigninputdata,
            "functional"
            )
    return functionaldesign

@app.post("/generatehighleveldesign")
def generate_high_level_design(highleveldesigninputdata: HighLevelDesignInput):
    '''Generate a high level design for given business context'''
    highleveldesign = GenLiteDesign(
        industry="healthcare"
        ).generate_high_level_design(
            highleveldesigninputdata,
            "highlevel"
            )
    return highleveldesign

@app.post("/generatelowleveldesign")
def generate_low_level_design(lowleveldesigninputdata: LowLevelDesignInput):
    '''Generate a low level design for given business context'''
    lowleveldesign = GenLiteDesign(
        industry="healthcare"
        ).generate_low_level_design(
            lowleveldesigninputdata,
            "lowlevel"
            )
    return lowleveldesign

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
