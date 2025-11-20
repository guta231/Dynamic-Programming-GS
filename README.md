# UpSkill AI: Otimizador de Treinamento (Dynamic Programming)

> **Global Solution - Future at Work**
>
> Solução em Python utilizando **Programação Dinâmica** para otimização de orçamento de treinamento corporativo.

## O Problema (Formulação)

No contexto do **Futuro do Trabalho**, empresas precisam decidir quais cursos oferecer aos funcionários para maximizar o aprendizado com um orçamento limitado.

* **Entrada:**
    1.  Lista de cursos vindos do banco de dados (cada um com `custo` e `impacto_skill`).
    2.  Orçamento total disponível do departamento.
* **Saída:** Lista ótima de cursos a serem contratados.
* **Objetivo:** Maximizar a soma total de `impacto_skill` respeitando o limite do `orcamento`.

---

## Como Executar

O projeto consiste em um script Python (`otimizador_upskill.py`) e um arquivo de banco de dados SQLite (`upskill.db`) que já contém os dados de teste.

### 1. Pré-requisitos
Instale as dependências necessárias:

```bash
pip install pandas sqlalchemy
```

### 2. Execução
Certifique-se de que o arquivo upskill.db está na mesma pasta do script. Execute no terminal:

```bash
python otimizador_upskill.py
```

## Estruturas e Algoritmos Utilizados

##Conforme solicitado nos requisitos da disciplina, a solução implementa as seguintes estruturas:

### 1. Estrutura de Ordenação (Merge Sort)
Implementamos o algoritmo Merge Sort (def merge_sort) para ordenar o DataFrame de cursos.

Lógica: Utiliza a abordagem "Dividir para Conquistar", dividindo a lista recursivamente e combinando-a de forma ordenada.

Uso: Demonstrado no início da execução para listar cursos por ordem de custo.

### 2. Recursão e Memoização
A função principal de otimização utiliza recursão para explorar a árvore de decisão.

Memoização: Utilizamos o decorador @lru_cache(None) para armazenar em cache os resultados de subproblemas já resolvidos. Isso evita o recálculo desnecessário e garante a performance exigida.

### 3. A Ideia da Mochila (Knapsack Problem)
A lógica central (def otimizar_orcamento) modela o cenário como o Problema da Mochila 0/1:

O algoritmo decide, item a item, se deve incluir o curso na "mochila" (orçamento) ou não.

Ele compara o ganho de incluir o curso versus o ganho de ignorá-lo, retornando sempre o maior valor de impacto possível.

# Autores
* Gustavo Henriqu de Oliveira - RM: 556712
* Gabriel Miranda - RM: 559102
* Gustavo Berlanga - RM: 555298
