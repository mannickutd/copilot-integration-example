from sqlalchemy.orm import Session
from . import models, schemas
from uuid import uuid4, UUID
from typing import List, Optional
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException


def get_client(db: Session, client_id: str) -> Optional[models.Client]:
    try:
        # Convert string to UUID if needed
        if isinstance(client_id, str):
            client_uuid = UUID(client_id)
        else:
            client_uuid = client_id
        return db.query(models.Client).filter(models.Client.id == client_uuid).first()
    except ValueError:
        # Invalid UUID format
        return None


def get_clients(db: Session, skip: int = 0, limit: int = 100) -> List[models.Client]:
    return db.query(models.Client).offset(skip).limit(limit).all()


def create_client(db: Session, client: schemas.ClientCreate) -> models.Client:
    try:
        db_client = models.Client(id=uuid4(), name=client.name)
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        return db_client
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Client name already exists")


def update_client(db: Session, client_id: str, client: schemas.ClientCreate) -> Optional[models.Client]:
    try:
        db_client = get_client(db, client_id)
        if db_client:
            db_client.name = client.name
            db.commit()
            db.refresh(db_client)
        return db_client
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Client name already exists")


def delete_client(db: Session, client_id: str) -> bool:
    db_client = get_client(db, client_id)
    if db_client:
        db.delete(db_client)
        db.commit()
        return True
    return False


def get_network(db: Session, network_id: int) -> Optional[models.Network]:
    return db.query(models.Network).filter(models.Network.id == network_id).first()


def get_networks(db: Session, skip: int = 0, limit: int = 100) -> List[models.Network]:
    return db.query(models.Network).offset(skip).limit(limit).all()


def create_network(db: Session, network: schemas.NetworkCreate) -> models.Network:
    try:
        db_network = models.Network(ipv4=network.ipv4)
        db.add(db_network)
        db.commit()
        db.refresh(db_network)
        return db_network
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Network IPv4 already exists")


def update_network(db: Session, network_id: int, network: schemas.NetworkCreate) -> Optional[models.Network]:
    try:
        db_network = get_network(db, network_id)
        if db_network:
            db_network.ipv4 = network.ipv4
            db.commit()
            db.refresh(db_network)
        return db_network
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Network IPv4 already exists")


def delete_network(db: Session, network_id: int) -> bool:
    db_network = get_network(db, network_id)
    if db_network:
        db.delete(db_network)
        db.commit()
        return True
    return False