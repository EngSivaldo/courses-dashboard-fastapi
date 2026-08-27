from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from models import CursoModel, CursoSchema

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Libera o acesso para que qualquer página web (Front-end) consiga conversar com a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Permite GET, POST, PUT, DELETE
    allow_headers=["*"],
)


@app.get('/cursos')
async def get_cursos(db: Session = Depends(get_db)):
    """Busca todos os cursos cadastrados no banco de dados."""
    cursos = db.query(CursoModel).all()
    return cursos


@app.get('/cursos/{cursoId}')
async def get_curso(cursoId: int, db: Session = Depends(get_db)):
    """Busca um curso específico pelo seu ID no banco de dados."""
    curso = db.query(CursoModel).filter(CursoModel.id == cursoId).first()
    
    if not curso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='Curso não encontrado.'
        )
        
    return curso


@app.post('/cursos', status_code=status.HTTP_201_CREATED)
async def post_curso(curso: CursoSchema, db: Session = Depends(get_db)):
    """Cadastra um novo curso no banco de dados. O ID é gerado automaticamente pelo banco."""
    # Instancia o objeto do banco sem precisar passar o ID manualmente
    novo_curso = CursoModel(
        titulo=curso.titulo,
        aulas=curso.aulas,
        horas=curso.horas
    )
    
    db.add(novo_curso)       # Prepara a gravação no banco
    db.commit()            # Executa e grava permanentemente
    db.refresh(novo_curso)  # Atualiza a instância com o 'id' gerado pelo banco
    
    return novo_curso

@app.put('/cursos/{cursoId}')
async def put_curso(cursoId: int, curso: CursoSchema, db: Session = Depends(get_db)):
    """Atualiza os dados de um curso existente no banco de dados."""
    # 1. Busca o curso no banco pelo ID
    curso_db = db.query(CursoModel).filter(CursoModel.id == cursoId).first()
    
    # 2. Se não encontrar, lança erro 404
    if not curso_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='Curso não encontrado.'
        )
        
    # 3. Atualiza os campos do objeto do banco com os novos valores recebidos
    curso_db.titulo = curso.titulo
    curso_db.aulas = curso.aulas
    curso_db.horas = curso.horas
    
    # 4. Salva as alterações no banco de dados
    db.commit()
    db.refresh(curso_db)
    
    return curso_db


@app.delete('/cursos/{cursoId}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(cursoId: int, db: Session = Depends(get_db)):
    """Deleta um curso do banco de dados pelo seu ID."""
    # 1. Busca o curso no banco
    curso_db = db.query(CursoModel).filter(CursoModel.id == cursoId).first()
    
    # 2. Se não existir, retorna 404
    if not curso_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='Curso não encontrado.'
        )
        
    # 3. Remove do banco e confirma a transação
    db.delete(curso_db)
    db.commit()
    
    # Retorna resposta vazia acompanhada do código 204
    return None

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)