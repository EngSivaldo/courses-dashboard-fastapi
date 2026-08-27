from typing import Optional
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import Column, Integer, String
from database import Base

# 1. Modelo da Tabela do Banco de Dados (SQLAlchemy)
class CursoModel(Base):
    __tablename__ = "cursos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    titulo = Column(String, nullable=False)
    aulas = Column(Integer, nullable=False)
    horas = Column(Integer, nullable=False)
    categoria = Column(String, nullable=False, default="Outros")


# 2. Esquemas de Validação da API (Pydantic)
class CursoBase(BaseModel):
    titulo: str = Field(..., min_length=3, max_length=100, description="Título do curso")
    aulas: int = Field(..., gt=0, description="Quantidade de aulas (maior que zero)")
    horas: int = Field(..., gt=0, description="Carga horária em horas (maior que zero)")
    categoria: str = Field(default="Outros", description="Tecnologia ou categoria do curso")

    @field_validator('titulo')
    @classmethod
    def validar_titulo_nao_vazio(cls, value: str) -> str:
        string_limpa = value.strip()
        if not string_limpa:
            raise ValueError('O título não pode ser vazio ou conter apenas espaços.')
        return string_limpa

class CursoCreate(CursoBase):
    pass

class CursoSchema(CursoBase):
    id: Optional[int] = None

    class Config:
        from_attributes = True