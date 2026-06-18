import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Carrega as variáveis do .env antes de importar os arquivos que as utilizam
load_dotenv()

from config.database import connect_db
from routes.monitoria_routes import router as monitoria_router

# Gerencia eventos de inicialização e desligamento
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Executa ao iniciar
    await connect_db()
    yield

app = FastAPI(lifespan=lifespan)

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(monitoria_router, prefix="/monitoria")

if __name__ == "__main__":
    # Inicia o servidor na porta 3000
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)