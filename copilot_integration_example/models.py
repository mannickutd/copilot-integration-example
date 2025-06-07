from sqlalchemy import Column, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Client(Base):
    __tablename__ = "client"

    id = Column(UUID, primary_key=True)
    name = Column(Text, nullable=False, unique=True)


class Network(Base):
    __tablename__ = "network"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ipv4 = Column(String(18), unique=True)


class ClientNetwork(Base):
    __tablename__ = "client_network"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(UUID, ForeignKey("client.id", ondelete="CASCADE"), nullable=False)
    network_id = Column(Integer, ForeignKey("network.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (UniqueConstraint("client_id", "network_id"),)
