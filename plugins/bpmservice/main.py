'''Main module for the FastAPI application'''
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from plugins.bpmservice.controller import GenLiteBPM
from plugins.bpmservice.model import BPMInput

app = FastAPI()
cors = CORSMiddleware(
    app,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
    )
app.add_middleware(cors)

@app.get("/processflow")
def generateprocessflow(bpminput: BPMInput):
    '''Index page'''

    bpmobject = GenLiteBPM(bpminput.industry)
    processflow = bpmobject.processflow_generate(bpminput)
    return {"processflow": processflow}

@app.get("/processflowasync")
async def generateprocessflowasync(bpminput: BPMInput):
    '''Index page'''

    bpmobject = GenLiteBPM(bpminput.industry)
    processflow = await bpmobject.processflow_generate_async(bpminput)
    return {"processflow": processflow}

@app.get("/bpmjson")
def generatebpmjson(bpminput: BPMInput):
    '''Index page'''

    bpmobject = GenLiteBPM(bpminput.industry)
    bpmjson = bpmobject.bpmjson_generate(bpminput)
    return {"bpmjson": bpmjson}

@app.get("/bpmjsonasync")
async def generatebpmjsonasync(bpminput: BPMInput):
    '''Index page'''

    bpmobject = GenLiteBPM(bpminput.industry)
    bpmjson = await bpmobject.bpmjson_generate_async(bpminput)
    return {"bpmjson": bpmjson}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
