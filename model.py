from typing import List, Optional
from sqlalchemy import Table, Column, ForeignKey, String, Integer, Boolean, Date, create_engine
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker, Mapped, mapped_column

# rose = clé primaire 
# 2 roses clés primaire composite
# Rouge = contrainte d'unisité. ça doit etre que une fois ensemble
# organisme en premier 
# titre bleu je peux les faire indépendaments des autres 
# 














class Base(DeclarativeBase):
    pass

# Table d'association pour la relation many-to-many
association_table = Table(
    "association_table",
    Base.metadata,
    Column("formation_id", ForeignKey("formation.id_formation"), primary_key=True),
    Column("format_code", ForeignKey("rncp.format_code"), primary_key=True),
)

class Formation(Base):
    __tablename__ = "formation"
    id_formation: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    url: Mapped[str] = mapped_column(String(100))
    
    # Relation one-to-many avec Session
    sessions: Mapped[List["Session"]] = relationship("Session", back_populates="formation")
    
    # Relation many-to-many avec Rncp
    rncps: Mapped[List["Rncp"]] = relationship(
        secondary=association_table, back_populates="formations"
    )

class Session(Base):
    __tablename__ = "session"
    id_session: Mapped[int] = mapped_column(primary_key=True)
    session_name: Mapped[str] = mapped_column(String(100))
    formation_id: Mapped[int] = mapped_column(ForeignKey("formation.id_formation"))
    duree: Mapped[int] = mapped_column(Integer)
    niveau: Mapped[str] = mapped_column(String(100))
    location: Mapped[str] = mapped_column(String(100))
    date_limite_candidature: Mapped[str] = mapped_column(String(100)) # à changer en date
    date_debut: Mapped[str] = mapped_column(String(100)) # à changer en date
    alternance: Mapped[bool] = mapped_column(Boolean)

    # Relation inverse one-to-many avec Formation
    formation: Mapped["Formation"] = relationship("Formation", back_populates="sessions")

class Rncp(Base):
    __tablename__ = "rncp"
    format_code: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    
    # Relation many-to-many avec Formation
    formations: Mapped[List["Formation"]] = relationship(
        secondary=association_table, back_populates="rncps"
    )