import uvicorn

def start():
    uvicorn.run("app.api.main:app", host="0.0.0.0", port=8000, reload=True)