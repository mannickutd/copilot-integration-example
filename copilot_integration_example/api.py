from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import clients, networks

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to restrict origins if needed
    allow_credentials=False,  # Set to False if allow_origins remains ["*"], or list specific origins if True
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"]
)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Include routers
app.include_router(clients.router)
app.include_router(networks.router)
