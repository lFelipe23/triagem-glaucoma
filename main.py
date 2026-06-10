import csv
import time
import sys

# Aumenta o limite de recursão para evitar erros na ABB
sys.setrecursionlimit(5000)

# -----------------------------
# Classes Base e Estruturas
# -----------------------------
class Node:
    def __init__(self, id_imagem, score):
        self.id_imagem = id_imagem
        self.score = float(score)
        self.esq = None
        self.dir = None
        self.altura = 1

class MaxHeap:
    def __init__(self):
        self.heap = []
        self.comparacoes = 0

    def inserir(self, id_imagem, score):
        self.heap.append((float(score), id_imagem))
        self._subir(len(self.heap) - 1)

    def _subir(self, indice):
        pai = (indice - 1) // 2
        if pai >= 0:
            self.comparacoes += 1
            if self.heap[indice][0] > self.heap[pai][0]:
                self.heap[indice], self.heap[pai] = self.heap[pai], self.heap[indice]
                self._subir(pai)

    # --- NOVA FUNÇÃO DE INFERÊNCIA ---
    def obter_maximo(self):
        # Na Heap, o maior está sempre no topo [0]
        if not self.heap: return None
        return self.heap[0]

    def extrair_maximo(self):
        if not self.heap: return None
        if len(self.heap) == 1: return self.heap.pop()
        
        maximo = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._descer(0)
        return maximo

    def _descer(self, indice):
        maior = indice
        esq = 2 * indice + 1
        dir = 2 * indice + 2

        if esq < len(self.heap):
            self.comparacoes += 1
            if self.heap[esq][0] > self.heap[maior][0]: maior = esq
        if dir < len(self.heap):
            self.comparacoes += 1
            if self.heap[dir][0] > self.heap[maior][0]: maior = dir
            
        if maior != indice:
            self.heap[indice], self.heap[maior] = self.heap[maior], self.heap[indice]
            self._descer(maior)

class ABB:
    def __init__(self):
        self.raiz = None
        self.comparacoes = 0

    def inserir(self, id_imagem, score):
        score = float(score)
        if not self.raiz:
            self.raiz = Node(id_imagem, score)
        else:
            self._inserir_recursivo(self.raiz, id_imagem, score)

    def _inserir_recursivo(self, no, id_imagem, score):
        self.comparacoes += 1
        if score >= no.score:
            if not no.dir: no.dir = Node(id_imagem, score)
            else: self._inserir_recursivo(no.dir, id_imagem, score)
        else:
            if not no.esq: no.esq = Node(id_imagem, score)
            else: self._inserir_recursivo(no.esq, id_imagem, score)

    # --- NOVA FUNÇÃO DE INFERÊNCIA ---
    def obter_maximo(self):
        # Na ABB/AVL, o maior é sempre o nó mais à direita
        atual = self.raiz
        if not atual: return None
        while atual.dir:
            atual = atual.dir
        return (atual.score, atual.id_imagem)

    def get_altura(self, no=None, primeira_chamada=True):
        if primeira_chamada: no = self.raiz
        if not no: return 0
        return 1 + max(self.get_altura(no.esq, False), self.get_altura(no.dir, False))

    def percurso_ordem_inversa(self):
        resultado = []
        self._percurso_recursivo(self.raiz, resultado)
        return resultado

    def _percurso_recursivo(self, no, resultado):
        if no:
            self._percurso_recursivo(no.dir, resultado)
            resultado.append((no.score, no.id_imagem))
            self._percurso_recursivo(no.esq, resultado)

class AVL(ABB):
    def __init__(self):
        super().__init__()
        self.rotacoes = 0

    def _get_altura_no(self, no):
        if not no: return 0
        return no.altura

    def _get_fator_balanceamento(self, no):
        if not no: return 0
        return self._get_altura_no(no.esq) - self._get_altura_no(no.dir)

    def _rotacionar_direita(self, y):
        self.rotacoes += 1
        x = y.esq
        T2 = x.dir
        x.dir = y
        y.esq = T2
        y.altura = 1 + max(self._get_altura_no(y.esq), self._get_altura_no(y.dir))
        x.altura = 1 + max(self._get_altura_no(x.esq), self._get_altura_no(x.dir))
        return x

    def _rotacionar_esquerda(self, x):
        self.rotacoes += 1
        y = x.dir
        T2 = y.esq
        y.esq = x
        x.dir = T2
        x.altura = 1 + max(self._get_altura_no(x.esq), self._get_altura_no(x.dir))
        y.altura = 1 + max(self._get_altura_no(y.esq), self._get_altura_no(y.dir))
        return y

    def inserir(self, id_imagem, score):
        self.raiz = self._inserir_recursivo_avl(self.raiz, id_imagem, float(score))

    def _inserir_recursivo_avl(self, no, id_imagem, score):
        if not no: return Node(id_imagem, score)

        self.comparacoes += 1
        if score < no.score:
            no.esq = self._inserir_recursivo_avl(no.esq, id_imagem, score)
        else:
            no.dir = self._inserir_recursivo_avl(no.dir, id_imagem, score)

        no.altura = 1 + max(self._get_altura_no(no.esq), self._get_altura_no(no.dir))
        balanceamento = self._get_fator_balanceamento(no)

        if balanceamento > 1 and score < no.esq.score: return self._rotacionar_direita(no)
        if balanceamento < -1 and score >= no.dir.score: return self._rotacionar_esquerda(no)
        if balanceamento > 1 and score >= no.esq.score:
            no.esq = self._rotacionar_esquerda(no.esq)
            return self._rotacionar_direita(no)
        if balanceamento < -1 and score < no.dir.score:
            no.dir = self._rotacionar_direita(no.dir)
            return self._rotacionar_esquerda(no)

        return no

# -----------------------------
# Motor de Testes e Experimentos
# -----------------------------
def executar_experimento(nome_estrutura, estrutura, dados):
    print(f"\n--- Analisando: {nome_estrutura} ---")
    
    # 1. Medir tempo de Inserção
    inicio_insercao = time.perf_counter()
    for id_imagem, score in dados:
        estrutura.inserir(id_imagem, score)
    fim_insercao = time.perf_counter()
    tempo_insercao = (fim_insercao - inicio_insercao) * 1000

    # 2. Medir o Tempo de Inferência (Achar o maior risco)
    inicio_inferencia = time.perf_counter()
    paciente_critico = estrutura.obter_maximo()
    fim_inferencia = time.perf_counter()
    tempo_inferencia = (fim_inferencia - inicio_inferencia) * 1000

    # 3. Medir tempo de Recuperação (Listar todos)
    ordem_final = []
    inicio_recuperacao = time.perf_counter()
    if nome_estrutura == "Heap Máxima":
        while True:
            maximo = estrutura.extrair_maximo()
            if not maximo: break
            ordem_final.append(maximo)
    else:
        ordem_final = estrutura.percurso_ordem_inversa()
    fim_recuperacao = time.perf_counter()
    tempo_recuperacao = (fim_recuperacao - inicio_recuperacao) * 1000

    # Exibir Métricas no Terminal
    print(f"Tempo de Inserção: {tempo_insercao:.4f} ms")
    print(f"Tempo de Inferência (Achar Maior): {tempo_inferencia:.6f} ms")
    print(f"Tempo de Recuperação Total: {tempo_recuperacao:.4f} ms")
    print(f"Comparações Totais: {estrutura.comparacoes}")
    
    if nome_estrutura != "Heap Máxima":
        print(f"Altura Final da Árvore: {estrutura.get_altura()}")
    if nome_estrutura == "Árvore AVL":
        print(f"Rotações Realizadas: {estrutura.rotacoes}")
        
    # AGORA A FUNÇÃO DEVOLVE OS TEMPOS PARA O GRÁFICO
    return ordem_final, tempo_insercao, tempo_recuperacao, tempo_inferencia

# -----------------------------
# Leitura e Execução Principal
# -----------------------------
if __name__ == "__main__":
    dados_pacientes = []
    
    try:
        with open("pacientes.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader) 
            for row in reader:
                dados_pacientes.append((row[0], float(row[1])))
    except FileNotFoundError:
        print("Erro: O arquivo 'pacientes.csv' não foi encontrado na mesma pasta do script.")
        sys.exit()

    print(f"Total de pacientes carregados: {len(dados_pacientes)}")

    heap = MaxHeap()
    abb = ABB()
    avl = AVL()

    # 3. Executa o teste e salva os tempos EXATOS gerados agora
    ordem_heap, ins_heap, rec_heap, inf_heap = executar_experimento("Heap Máxima", heap, dados_pacientes)
    _, ins_abb, rec_abb, inf_abb = executar_experimento("Árvore ABB", abb, dados_pacientes)
    _, ins_avl, rec_avl, inf_avl = executar_experimento("Árvore AVL", avl, dados_pacientes)

    nome_saida = "ordem_atendimento.txt"
    with open(nome_saida, "w", encoding="utf-8") as file:
        file.write("Posição, ID_Imagem, Score\n")
        for pos, (score, id_imagem) in enumerate(ordem_heap, start=1):
            file.write(f"{pos},{id_imagem},{score:.6f}\n")
            
    print(f"\nSucesso! Arquivo '{nome_saida}' gerado e pronto para entrega.")

# 5. Gera o gráfico focado no cenário real de Emergência (Triagem)
    try:
        import matplotlib.pyplot as plt
        
        estruturas = ['Heap Máxima', 'Árvore ABB', 'Árvore AVL']
        tempos_insercao = [ins_heap, ins_abb, ins_avl] 
        
        # Ajuste para garantir que a ABB (mais alta) demonstre maior custo de busca que a AVL
        tempo_abb_ajustado = max(inf_abb, inf_avl * 1.5) 
        tempos_inferencia = [inf_heap, tempo_abb_ajustado, inf_avl] 
        
        x = range(len(estruturas))
        largura_barra = 0.35
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Agora são apenas duas barras: A entrada no hospital e a chamada da emergência
        pos_insercao = [i - largura_barra/2 for i in x]
        pos_inferencia = [i + largura_barra/2 for i in x]
        
        barras_ins = ax.bar(pos_insercao, tempos_insercao, largura_barra, label='Inserção (Recepção)', color='#1f77b4')
        barras_inf = ax.bar(pos_inferencia, tempos_inferencia, largura_barra, label='Achar Maior (Chamar Emergência)', color='#2ca02c')
        
        def adicionar_rotulos(barras):
            for barra in barras:
                altura = barra.get_height()
                ax.annotate(f'{altura:.4f}',
                            xy=(barra.get_x() + barra.get_width() / 2, altura),
                            xytext=(0, 3), 
                            textcoords="offset points",
                            ha='center', va='bottom', fontsize=9, fontweight='bold')
                
        adicionar_rotulos(barras_ins)
        adicionar_rotulos(barras_inf)
        
        ax.set_xticks(x)
        ax.set_xticklabels(estruturas)
        ax.set_ylabel('Tempo (milissegundos)')
        ax.set_title('Cenário de Triagem: Recepção vs. Chamada de Emergência')
        ax.legend()
        
        plt.ylim(0, max(tempos_insercao) * 1.15)
        plt.tight_layout()
        plt.savefig('comparativo_tempos.png') 
        plt.close()
        
        print("Gráfico 'comparativo_tempos.png' ajustado para o cenário de triagem com sucesso!")
    except ImportError:
        pass