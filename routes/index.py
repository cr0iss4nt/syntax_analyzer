import logging
from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

index_router = APIRouter(prefix="", tags=["index"])
templates = Jinja2Templates(directory="templates/")

@index_router.get('/', response_class=HTMLResponse)
async def index(request:Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={}
    )