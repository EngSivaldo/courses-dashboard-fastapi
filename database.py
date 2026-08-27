from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Define o local do banco de dados (criará o arquivo 'cursos.db' no mesmo diretório)
SQLALCHEMY_DATABASE_URL = "sqlite:///./cursos.db"

# Engine de conexão do SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Cria a fábrica de sessões do banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base para a criação dos modelos da tabela
Base = declarative_base()

# Função Utilitária para abrir e fechar a conexão do banco por requisição
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()