from typing import Optional
from fastapi import FastAPI, HTTPException, status, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from models import CursoModel, CursoSchema

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/cursos')
async def get_cursos(
    q: Optional[str] = Query(None, description="Filtrar cursos por palavra-chave no título ou categoria"),
    limit: int = Query(10, gt=0, le=100, description="Quantidade máxima de registros por página"),
    offset: int = Query(0, ge=0, description="Quantidade de registros para pular (paginação)"),
    db: Session = Depends(get_db)
):
    """Busca cursos cadastrados com suporte a busca por palavra-chave e paginação."""
    query = db.query(CursoModel)
    
    if q:
        termo_busca = f"%{q.strip()}%"
        query = query.filter(
            (CursoModel.titulo.ilike(termo_busca)) | 
            (CursoModel.categoria.ilike(termo_busca))
        )
        
    cursos = query.offset(offset).limit(limit).all()
    return cursos


@app.get('/cursos/{cursoId}')
async def get_curso(cursoId: int, db: Session = Depends(get_db)):
    """Busca um curso específico pelo seu ID."""
    curso = db.query(CursoModel).filter(CursoModel.id == cursoId).first()
    
    if not curso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='Curso não encontrado.'
        )
        
    return curso


@app.post('/cursos', status_code=status.HTTP_201_CREATED)
async def post_curso(curso: CursoSchema, db: Session = Depends(get_db)):
    """Cadastra um novo curso incluindo a categoria."""
    novo_curso = CursoModel(
        titulo=curso.titulo,
        aulas=curso.aulas,
        horas=curso.horas,
        categoria=curso.categoria
    )
    
    db.add(novo_curso)
    db.commit()
    db.refresh(novo_curso)
    
    return novo_curso


@app.put('/cursos/{cursoId}')
async def put_curso(cursoId: int, curso: CursoSchema, db: Session = Depends(get_db)):
    """Atualiza os dados de um curso existente."""
    curso_db = db.query(CursoModel).filter(CursoModel.id == cursoId).first()
    
    if not curso_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='Curso não encontrado.'
        )
        
    curso_db.titulo = curso.titulo
    curso_db.aulas = curso.aulas
    curso_db.horas = curso.horas
    curso_db.categoria = curso.categoria
    
    db.commit()
    db.refresh(curso_db)
    
    return curso_db


@app.delete('/cursos/{cursoId}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(cursoId: int, db: Session = Depends(get_db)):
    """Deleta um curso pelo seu ID."""
    curso_db = db.query(CursoModel).filter(CursoModel.id == cursoId).first()
    
    if not curso_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='Curso não encontrado.'
        )
        
    db.delete(curso_db)
    db.commit;
    
    return None


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)