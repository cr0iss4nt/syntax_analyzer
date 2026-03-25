import logging

import uvicorn
from fastapi import FastAPI, Request

from routes.analysis import analysis_router
from routes.index import index_router
from routes.info import info_router

app = FastAPI(title="Syntax Analyzer")

app.include_router(index_router)
app.include_router(info_router)
app.include_router(analysis_router)

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)