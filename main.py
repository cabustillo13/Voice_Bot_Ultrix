from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn

import time


app = FastAPI()

# Mount the static directory to serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the index.html file
@app.get("/", response_class=HTMLResponse)
async def read_index():
    """Index main page"""
    with open("static/index.html", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)


@app.post("/process_text")
async def process_text(request: Request):
    """Ask to agent and return the answer"""
    data = await request.json()
    input_text = data.get("text", "")
    
    # Process input data
    processed_text = f"Answer: {input_text}"

    time.sleep(5)

    return JSONResponse(content={"text": processed_text})


# It runs in http://127.0.0.1:8000 or http://0.0.0.0:8000
if __name__ == '__main__':

    # 0.0.0.0 or 127.0.0.1
    uvicorn.run(app, host='127.0.0.1', port=8000)
