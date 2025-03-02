from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def status():
    return {"Status": "Operational"}

@app.post("/new-incident")
def newIncident():
    return {"Status": "In progress"}

@app.get("/get-incidents")
def getIncidents():
    return {"Status": "In progress"}