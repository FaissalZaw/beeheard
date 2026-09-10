from fastapi import FastAPI

app = FastAPI(title="BeeHeard")

@app.get("/")
def racine():
    return {"statut": "ok", "projet": "BeeHeard"}
