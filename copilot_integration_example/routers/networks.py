from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db

router = APIRouter()


@router.post("/networks", response_model=schemas.Network)
def create_network(network: schemas.NetworkCreate, db: Session = Depends(get_db)):
    return crud.create_network(db=db, network=network)


@router.get("/networks", response_model=List[schemas.Network])
def read_networks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_networks(db, skip=skip, limit=limit)


@router.get("/networks/{network_id}", response_model=schemas.Network)
def read_network(network_id: int, db: Session = Depends(get_db)):
    db_network = crud.get_network(db, network_id=network_id)
    if db_network is None:
        raise HTTPException(status_code=404, detail="Network not found")
    return db_network


@router.put("/networks/{network_id}", response_model=schemas.Network)
def update_network(network_id: int, network: schemas.NetworkCreate, db: Session = Depends(get_db)):
    db_network = crud.update_network(db, network_id=network_id, network=network)
    if db_network is None:
        raise HTTPException(status_code=404, detail="Network not found")
    return db_network


@router.delete("/networks/{network_id}")
def delete_network(network_id: int, db: Session = Depends(get_db)):
    success = crud.delete_network(db, network_id=network_id)
    if not success:
        raise HTTPException(status_code=404, detail="Network not found")
    return {"message": "Network deleted successfully"}