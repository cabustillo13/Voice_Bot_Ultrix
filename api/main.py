from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn

from api.agent.main_pipeline import agent_executor


app = FastAPI()

# Mount the static directory to serve static files
app.mount("/static", StaticFiles(directory="./api/static"), name="static")

# Serve the index.html file
@app.get("/", response_class=HTMLResponse)
async def read_index():
    """Index main page"""
    with open("./api/static/index.html", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)


@app.post("/process_text")
async def process_text(request: Request):
    """Ask to agent and return the answer"""
    data = await request.json()
    user_question = data.get("text", "")
    
    # Process input data
    processed_text = agent_executor.invoke({
        "input": user_question,
        "chat_history": [],
        })

    print(processed_text)

    return JSONResponse(content={"text": processed_text["output"]})


# It runs in http://127.0.0.1:8000 or http://0.0.0.0:8000
if __name__ == '__main__':

    # 0.0.0.0 or 127.0.0.1
    uvicorn.run(app, host='127.0.0.1', port=8000)
