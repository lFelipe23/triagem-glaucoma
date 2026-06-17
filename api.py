from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import List
import uuid
import time
import heapq
import io
from PIL import Image

# ==========================================
# 1. MODELOS PYDANTIC (VALIDAÇÃO DE RESPOSTA)
# ==========================================
class PacienteResponse(BaseModel):
    posicao: int
    id: str
    nome: str
    idade: int
    risco: float

# ==========================================
# 2. SIMULAÇÃO DO MODELO DE DEEP LEARNING
# ==========================================
def predict_risk(image_bytes: bytes) -> float:
    """Simula a predição. Falha intencional se o modelo estiver 'fora do ar'."""
    try:
        import random
        # Retorna um valor de risco fictício entre 0.0 e 1.0
        return round(random.uniform(0.1, 0.99), 4)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Modelo DL indisponível")

# ==========================================
# 3. ESTRUTURA DA FILA (PRIORITY QUEUE)
# ==========================================
class PriorityQueue:
    def __init__(self):
        self.heap = []
        
    def push(self, risco: float, dados: dict):
        # A tupla usa (-risco, timestamp, dados) para forçar o heapq a atuar como Max-Heap
        # O timestamp previne erro de comparação entre dicionários se os riscos forem iguais
        timestamp = time.time()
        heapq.heappush(self.heap, (-risco, timestamp, dados))
        
    def pop(self) -> dict:
        if not self.heap:
            return None
        # Remove a tupla e retorna apenas os dados do paciente
        _, _, dados = heapq.heappop(self.heap)
        return dados
        
    def listar(self) -> List[dict]:
        # Ordena a heap pelo maior risco (o primeiro elemento da tupla já é negativo)
        copia_ordenada = sorted(self.heap)
        return [dados for _, _, dados in copia_ordenada]

# Instância global exigida
fila_atendimento = PriorityQueue()

# ==========================================
# 4. ENDPOINTS DA API
# ==========================================
app = FastAPI(title="Triagem Hospitalar IA")

@app.get("/api/fila", response_model=List[PacienteResponse])
async def get_fila():
    pacientes = fila_atendimento.listar()
    
    resultado = []
    for index, dados in enumerate(pacientes):
        resultado.append(
            PacienteResponse(
                posicao=index + 1,
                id=dados["id"],
                nome=dados["nome"],
                idade=dados["idade"],
                risco=dados["risco"]
            )
        )
    return resultado

@app.post("/api/chamar-proximo", response_model=PacienteResponse)
async def post_chamar_proximo():
    dados_paciente = fila_atendimento.pop()
    
    if not dados_paciente:
        # Retorno exato exigido pelo professor para fila vazia
        raise HTTPException(status_code=404, detail={"erro": "Fila vazia"})
        
    return PacienteResponse(
        posicao=1,
        id=dados_paciente["id"],
        nome=dados_paciente["nome"],
        idade=dados_paciente["idade"],
        risco=dados_paciente["risco"]
    )

@app.post("/api/upload", status_code=201)
async def post_upload(
    nome: str = Form(...),
    idade: int = Form(...),
    imagem: UploadFile = File(...)
):
    image_bytes = await imagem.read()
    
    # Validação do arquivo: Verifica se é realmente uma imagem usando PIL
    try:
        img = Image.open(io.BytesIO(image_bytes))
        img.verify()
    except Exception:
        raise HTTPException(status_code=400, detail="Arquivo inválido (não imagem)")
    
    # Processa o risco e gera UUID
    risco_calculado = predict_risk(image_bytes)
    id_unico = str(uuid.uuid4())
    
    dados_paciente = {
        "id": id_unico,
        "nome": nome,
        "idade": idade,
        "risco": risco_calculado
    }
    
    # Insere na PriorityQueue conforme formato do Módulo 4
    fila_atendimento.push(risco_calculado, dados_paciente)
    
    return {
        "status": "inserido",
        "id": id_unico,
        "risco": risco_calculado
    }