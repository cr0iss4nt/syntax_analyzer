import logging
from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

info_router = APIRouter(prefix="/info", tags=["info"])
templates = Jinja2Templates(directory="templates/")

@info_router.get('/', response_class=HTMLResponse)
async def info(request:Request):
    return templates.TemplateResponse(
        request=request, name="info.html", context={}
    )