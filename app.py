from fastapi import FastAPI, Request
from pydantic import BaseModel
from gradio_client import Client
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title="Text Summarizer",
    description="Text Summarizer using T5",
    version="1.0"
)

app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static"
)

templates = Jinja2Templates(directory=str(BASE_DIR))


# Connect to your Hugging Face Space
client = Client("HITESHCODER/text-summarizer-app")


class DialogueInput(BaseModel):
    dialogue: str


def summarize_dialogue(dialogue: str) -> str:

    result = client.predict(
        dialogue=dialogue,
        api_name="/summarize_dialogue"
    )

    return result


@app.post("/summarize/")
def summarize(dialogue_input: DialogueInput):

    summary = summarize_dialogue(dialogue_input.dialogue)

    return {"summary": summary}


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )
