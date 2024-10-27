import uvicorn

def start():
    uvicorn.run("app.api.main:app", host="localhost", port=8000, reload=True)