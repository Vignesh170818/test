'''Main module for the FastAPI application'''
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from plugins.userstoryservice.controller import GenLiteUserStory
from plugins.userstoryservice.model import UserStoryInput, ExpandUserStoryInput

app = FastAPI()
cors = CORSMiddleware(
    app,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
    )
app.add_middleware(cors)

@app.post("/generateuserstory")
def generate_user_story(userstoryinputdata: UserStoryInput):
    '''Generate a user story for given business context'''
    userstory = GenLiteUserStory(
        industry="healthcare"
        ).generate(userstoryinputdata)
    return userstory

@app.post("/expanduserstory")
def expand_user_story(userstoryinputdata: ExpandUserStoryInput):
    '''Expand a user story for given business context'''
    userstory = GenLiteUserStory(
        industry="healthcare"
        ).expand(userstoryinputdata)
    return userstory

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
