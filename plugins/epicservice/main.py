'''Main module for the FastAPI application'''
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from plugins.epicservice.controller import GenLiteEPIC
from plugins.epicservice.model import EPICInput, EPICReviewInput, EPICApplyReviewInput

app = FastAPI()
cors = CORSMiddleware(
    app,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
    )
app.add_middleware(cors)

@app.post("/generate")
def generateepic(epicinput: EPICInput):
    '''Index page'''

    epicobject = GenLiteEPIC(epicinput.industry)
    processflow = epicobject.generate(epicinput)
    return {"processflow": processflow}

@app.post("/review")
def reviewepic(epicinput: EPICReviewInput):
    '''Index page'''

    epicobject = GenLiteEPIC(epicinput.industry)
    processflow = epicobject.review(epicinput)
    return {"processflow": processflow}

@app.post("/applyreview")
def applyreviewepic(epicinput: EPICApplyReviewInput):
    '''Index page'''

    epicobject = GenLiteEPIC(epicinput.industry)
    processflow = epicobject.applyreview(epicinput)
    return {"processflow": processflow}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
