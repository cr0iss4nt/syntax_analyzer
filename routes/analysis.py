import logging
import os
import tempfile
import time

from fastapi import Request, APIRouter, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import modules.analyzer
from modules.file_parser import parse_file

analysis_router = APIRouter(prefix="/analysis", tags=["analysis"])
templates = Jinja2Templates(directory="templates/")

@analysis_router.post('/', response_class=HTMLResponse)
async def analyze(request: Request, file: UploadFile = File(...)):
    MAX_SIZE = 10 * 1024 * 1024
    content = await file.read()
    if len(content) > MAX_SIZE:
        raise HTTPException(status_code=413, detail="File too large")

    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(content)
        tmp_path = tmp_file.name

    try:
        text = parse_file(tmp_path)
    finally:
        os.unlink(tmp_path)

    t1 = time.time()
    analysis, svg = modules.analyzer.analyze(text)
    dt = round(time.time()-t1, 3)

    return templates.TemplateResponse(
        request=request, name="analysis.html", context={"analysis":analysis, "scheme":svg, "dt":dt}
    )