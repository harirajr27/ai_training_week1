from fastapi import FastAPI

# This variable must be named exactly 'app'
app = FastAPI(title="Mini CRUD API")

@app.get("/health")
def health_check():
    return {"status": "ok"}
