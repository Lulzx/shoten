import time
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from libgen_api import LibgenSearch
s = LibgenSearch()


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.get("/query/{query}")
async def read_item(query):
    start = time.time()
    title = query.lower()
    filters = {
        "Extension"	: "pdf"
    }
    result = s.search_title_filtered(title, filters)
    end = time.time()
    time_elapsed = end - start
    return {"results": result, "count": len(result), "time": time_elapsed}
