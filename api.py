from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from typing import List, Dict, Any
import time
import heapq

# ==========================================
# 1. INTEGRAÇÃO DO MODELO DE DEEP LEARNING
# ==========================================
def predict_risk(image_bytes: bytes) -> float:
    """
    Função simulada do modelo de Deep Learning.
    Na versão final, substitua por sua lógica real de predição (ex: PyTorch/TensorFlow).
    """
    import random
    # Retorna um valor de risco fictício entre 0.0 e 1.0
    return round(random.uniform(0.1, 0.99), 4)

# ==========================================
# 2. ESTRUTURA DE DADOS (HEAP MÁXIMA)
# ==========================================
class Paciente:
    def __init__(self, nome: str, idade: int, risco: float):
        self.nome = nome
        self.idade = idade
        self.risco = risco
        self.timestamp = time.time() # Critério de desempate: ordem de chegada

    def to_dict(self, posicao: int) -> Dict[str, Any]:
        return {
            "posicao": posicao,
            "nome": self.nome,
            "idade": self.idade,
            "risco": self.risco
        }

    # Sobrecarga de operadores para o heapq funcionar como Max Heap
    # Invertemos a lógica do "menor que" para que o maior risco fique no topo
    def __lt__(self, outro):
        if self.risco == outro.risco:
            # Em caso de empate no risco, ganha quem chegou primeiro (menor timestamp)
            return self.timestamp < outro.timestamp 
        return self.risco > outro.risco 

class FilaPrioridade:
    def __init__(self):
        self.heap = []
    
    def inserir(self, paciente: Paciente):
        heapq.heappush(self.heap, paciente)
        
    def chamar_proximo(self) -> Paciente:
        if not self.heap:
            return None
        return heapq.heappop(self.heap)
    
    def listar_ordenado(self) -> List[Paciente]:
        # Retorna uma cópia ordenada da fila sem destruir a Heap original
        # O(n log n) para ordenar apenas na hora de visualizar a tela
        return sorted(self.heap)

# Instância global da fila para manter os dados em memória enquanto a API roda
fila_hospital = FilaPrioridade()

# =========================================
# 3. ENDPOINTS DA API (FASTAPI)
# =========================================
app = FastAPI(
    title="API Triagem de Glaucoma",
    description="Backend para gerenciamento da fila de prioridade hospitalar via Heap Máxima.",
    version="1.0.0"
)

@app.get("/api/fila", summary="Lista a fila de pacientes")
async def get_fila():
    """
    Retorna a lista ordenada dos pacientes na fila, do maior risco para o menor.
    """
    pacientes_ordenados = fila_hospital.listar_ordenado()
    
    resultado = []
    for index, paciente in enumerate(pacientes_ordenados):
        resultado.append(paciente.to_dict(posicao=index + 1))
        
    return {"fila": resultado, "total_espera": len(resultado)}

@app.post("/api/chamar-proximo", summary="Chama o paciente mais grave")
async def post_chamar_proximo():
    """
    Remove e retorna o paciente mais prioritário do topo da fila.
    """
    paciente = fila_hospital.chamar_proximo()
    
    if not paciente:
        raise HTTPException(status_code=404, detail="A fila de atendimento está vazia.")
        
    return {
        "status": "chamado",
        "paciente": paciente.to_dict(posicao=0)
    }

@app.post("/api/upload", summary="Insere novo paciente e exame na fila")
async def post_upload(
    nome: str = Form(...),
    idade: int = Form(...),
    imagem: UploadFile = File(...)
):
    """
    Recebe os dados do exame, calcula o risco via DL e insere o paciente na Fila de Prioridade.
    """
    # Lemos os bytes da imagem enviada
    image_bytes = await imagem.read()
    
    # Passamos a imagem para o modelo de IA calcular o risco
    risco_calculado = predict_risk(image_bytes)
    
    # Criamos o objeto do paciente e inserimos na Heap Máxima
    novo_paciente = Paciente(nome=nome, idade=idade, risco=risco_calculado)
    fila_hospital.inserir(novo_paciente)
    
    return {
        "status": "inserido",
        "risco": risco_calculado,
        "mensagem": f"Paciente {nome} adicionado à fila com sucesso."
    }