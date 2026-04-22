import logging
import os
import tempfile
import time
import uuid
from fastapi import Request, APIRouter, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

import modules.analyzer
from modules.file_parser import parse_file

analysis_router = APIRouter(prefix="/analysis", tags=["analysis"])
templates = Jinja2Templates(directory="templates/")

_text_cache = {}
CACHE_TTL_SECONDS = 3600

def _clean_cache():
    now = time.time()
    expired = [k for k, v in _text_cache.items() if now - v["timestamp"] > CACHE_TTL_SECONDS]
    for k in expired:
        del _text_cache[k]

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
    analysis, svgs, entities = modules.analyzer.analyze_syntax(text)
    dt = round(time.time() - t1, 3)

    session_id = str(uuid.uuid4())
    _clean_cache()
    _text_cache[session_id] = {"text": text, "timestamp": time.time()}

    return templates.TemplateResponse(
        request=request,
        name="analysis.html",
        context={
            "analysis": analysis,
            "schemes": svgs,
            "dt": dt,
            "entities": entities,
            "session_id": session_id
        }
    )

@analysis_router.get("/ai/{session_id}")
async def get_ai_analysis(session_id: str):
    entry = _text_cache.get(session_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Session expired or not found")
    text = entry["text"]
    try:
        t1 = time.time()
        ai_result = modules.analyzer.analyze_ai(text)
        dt = time.time()-t1
        print(f"SEMANTIC AI ANALYSIS ({os.getenv('OPENROUTER_MODEL')}) DONE IN {dt:.3f} SECONDS")
        return JSONResponse(content=ai_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI analysis failed: {str(e)}")