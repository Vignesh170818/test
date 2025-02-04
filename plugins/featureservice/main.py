'''Main module for the FastAPI application'''
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from plugins.featureservice.controller import GenLiteFeature
from plugins.featureservice.model import FeatureInput, ExpandFeatureInput

app = FastAPI()
cors = CORSMiddleware(
    app,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
    )
app.add_middleware(cors)

@app.post("/generatefeature")
async def generate_feature(featureinput: FeatureInput):
    '''Generate a feature for given business context'''
    genlitefeature = GenLiteFeature(featureinput.industry)
    feature = genlitefeature.generate(featureinput)
    return {"feature": feature}

@app.post("/expandfeature")
async def expand_feature(featureinput: ExpandFeatureInput):
    '''Expand a feature for given business context'''
    genlitefeature = GenLiteFeature(featureinput.industry)
    feature = genlitefeature.expand(featureinput)
    return {"feature": feature}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
