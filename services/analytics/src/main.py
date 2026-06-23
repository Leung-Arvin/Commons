from fastapi import FastAPI

app = FastAPI(title="FloorSense Location Service")

@app.get("/health")
def health():
    return {"status": "ok"}
