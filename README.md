# Triagem de Glaucoma em Tempo Real 🏥👁️

Este repositório contém a implementação prática de um sistema de triagem clínica de urgência assistido por Inteligência Artificial para avaliação do risco de glaucoma. O projeto compara o desempenho de três estruturas de dados fundamentais (**Heap Máxima**, **Árvore Binária de Busca - ABB** e **Árvore AVL**) em um cenário de fluxo hospitalar crítico.

---

## 📌 Cenário do Projeto

Diferente de sistemas baseados em relatórios estáticos de fim de dia, o motor de triagem foca na dinâmica de um pronto-socorro real, avaliando duas operações cruciais:
1. **Recepção/Admissão (Inserção):** A velocidade para colocar o paciente porta para dentro do sistema com seu escore de prioridade gerado pela IA.
2. **Chamada de Emergência (Inferência):** O custo computacional para identificar e chamar instantaneamente o caso de maior gravidade na fila (operação com complexidade $O(1)$ na Heap Máxima).

---

## 📂 Estrutura do Repositório

O projeto está organizado da seguinte forma para manter a clareza e a modularidade:

* `main.py`: Código-fonte principal com as estruturas e simulação do ambiente hospitalar.
* `pacientes.csv`: Base de dados de teste contendo 1.020 registros de pacientes.
* `comparativo_tempos.png`: Gráfico de barras gerado pelo matplotlib focado no cenário de triagem.
* `ordem_atendimento.txt`: Arquivo de saída oficial gerado pela estrutura.
* `relatorio/`: Pasta contendo o Relatório Técnico final em PDF documentando a análise de complexidade.

---

## 🚀 Como Executar o Projeto

**Pré-requisitos:** Python 3.10+ instalado.

**1. Clonar o Repositório**
```bash
git clone https://github.com/IFelipe23/triagem-glaucoma.git
cd triagem-glaucoma
```

**2. Instalar Dependências**
```bash
pip install matplotlib
```

**3. Executar a Simulação**
```bash
python main.py
```

---

## 📊 Métricas e Resultados

Os testes práticos demonstram que a **Heap Máxima** consolida-se como a arquitetura ideal para o motor de triagem. Enquanto estruturas em árvore (como a AVL) demandam um alto custo operacional para manter o balanceamento perfeito na recepção, a Heap Máxima garante a inserção ágil e a chamada da emergência em tempo constante **$O(1)$**, visto que o paciente mais grave reside nativamente na raiz do vetor.

---

## 👥 Equipe Desenvolvedora

* Eduardo Arthur
* Eliabe Rafael
* Erik Jerônimo
* Joseildo dos Santos
* Luis Felipe

---

## 🎓 Contexto Acadêmico e Institucional

Este projeto foi desenvolvido com fins educacionais como parte dos requisitos práticos da disciplina de **Estruturas de Dados**, do curso de **Análise e Desenvolvimento de Sistemas (3º Período)** no **Instituto Federal de Pernambuco (IFPE) - Campus Palmares**. 
