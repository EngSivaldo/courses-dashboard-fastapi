from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from database import Base

# 1. Modelo da Tabela do Banco de Dados (SQLAlchemy)
class CursoModel(Base):
    __tablename__ = "cursos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    titulo = Column(String, nullable=False)
    aulas = Column(Integer, nullable=False)
    horas = Column(Integer, nullable=False)


# 2. Esquemas de Validação da API (Pydantic)
class CursoSchema(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: int
    horas: int

    class Config:
        from_attributes = True  # Permite conversão direta de objetos SQLAlchemy para Pydantic