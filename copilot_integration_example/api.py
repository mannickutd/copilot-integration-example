from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import crud, schemas
from .database import get_db

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Client endpoints
@app.post("/clients", response_model=schemas.Client)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    return crud.create_client(db=db, client=client)


@app.get("/clients", response_model=List[schemas.Client])
def read_clients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_clients(db, skip=skip, limit=limit)


@app.get("/clients/{client_id}", response_model=schemas.Client)
def read_client(client_id: str, db: Session = Depends(get_db)):
    db_client = crud.get_client(db, client_id=client_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client


@app.put("/clients/{client_id}", response_model=schemas.Client)
def update_client(client_id: str, client: schemas.ClientCreate, db: Session = Depends(get_db)):
    db_client = crud.update_client(db, client_id=client_id, client=client)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client


@app.delete("/clients/{client_id}")
def delete_client(client_id: str, db: Session = Depends(get_db)):
    success = crud.delete_client(db, client_id=client_id)
    if not success:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"message": "Client deleted successfully"}


# Network endpoints
@app.post("/networks", response_model=schemas.Network)
def create_network(network: schemas.NetworkCreate, db: Session = Depends(get_db)):
    return crud.create_network(db=db, network=network)


@app.get("/networks", response_model=List[schemas.Network])
def read_networks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_networks(db, skip=skip, limit=limit)


@app.get("/networks/{network_id}", response_model=schemas.Network)
def read_network(network_id: int, db: Session = Depends(get_db)):
    db_network = crud.get_network(db, network_id=network_id)
    if db_network is None:
        raise HTTPException(status_code=404, detail="Network not found")
    return db_network


@app.put("/networks/{network_id}", response_model=schemas.Network)
def update_network(network_id: int, network: schemas.NetworkCreate, db: Session = Depends(get_db)):
    db_network = crud.update_network(db, network_id=network_id, network=network)
    if db_network is None:
        raise HTTPException(status_code=404, detail="Network not found")
    return db_network


@app.delete("/networks/{network_id}")
def delete_network(network_id: int, db: Session = Depends(get_db)):
    success = crud.delete_network(db, network_id=network_id)
    if not success:
        raise HTTPException(status_code=404, detail="Network not found")
    return {"message": "Network deleted successfully"}
