from fastapi import FastAPI
from .routers import clients, networks

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Include routers
app.include_router(clients.router)
app.include_router(networks.router)
