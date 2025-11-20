import pandas as pd
from functools import lru_cache
from sqlalchemy import create_engine
import sys


# 1. CONFIGURAÇÃO DA CONEXÃO COM BANCO LOCAL


def conectar_db():
 
    try:
        
       #  Exemplo para SQLite (é um arquivo local):
        connection_string = "sqlite:///upskill.db"
        
        engine = create_engine(connection_string)
        
        # Testa a conexão
        with engine.connect() as conexao:
            print("--- Conexão com o Banco de Dados estabelecida com sucesso! ---")
        return engine
        
    except Exception as e:
        print(f"Erro: Não foi possível conectar ao banco de dados.")
        print(f"Detalhe do erro: {e}")
        print("Por favor, verifique sua 'connection_string' no script.")
        return None

# 2. FUNÇÕES DE BUSCA NO BANCO DE DADOS


def buscar_cursos(engine) -> pd.DataFrame:
    """
    Busca todos os cursos da tabela 'Cursos' e retorna um DataFrame.
    """
    print("Buscando lista de cursos no banco de dados...")
    try:
        # Puxa as 3 colunas que precisamos para o problema da mochila
        query = "SELECT nome_curso, custo, impacto_skill AS impacto FROM Cursos"
        df_cursos = pd.read_sql(query, engine)
        
        if df_cursos.empty:
            print("Aviso: A tabela 'Cursos' está vazia. Não há o que otimizar.")
        
        return df_cursos
        
    except Exception as e:
        print(f"Erro ao buscar cursos: {e}")
        return pd.DataFrame() # Retorna dataframe vazio

def buscar_departamentos(engine) -> pd.DataFrame:
    """
    Busca todos os departamentos para o usuário poder escolher.
    """
    try:
        query = "SELECT id_depto, nome_depto, orcamento_treinamento FROM Departamentos"
        df_deptos = pd.read_sql(query, engine)
        return df_deptos
        
    except Exception as e:
        print(f"Erro ao buscar departamentos: {e}")
        return pd.DataFrame()


# 3. ESTRUTURA DE ORDENAÇÃO (Merge Sort - Sem alterações)

def merge_sort(df: pd.DataFrame, column: str) -> pd.DataFrame:
    if len(df) <= 1:
        return df
    mid = len(df) // 2
    left_half = merge_sort(df.iloc[:mid], column)
    right_half = merge_sort(df.iloc[mid:], column)
    return _merge(left_half, right_half, column)

def _merge(left: pd.DataFrame, right: pd.DataFrame, column: str) -> pd.DataFrame:
    result = []
    i = j = 0
    left_records = left.to_dict('records')
    right_records = right.to_dict('records')
    while i < len(left_records) and j < len(right_records):
        if left_records[i][column] <= right_records[j][column]:
            result.append(left_records[i])
            i += 1
        else:
            result.append(right_records[j])
            j += 1
    result.extend(left_records[i:])
    result.extend(right_records[j:])
    return pd.DataFrame(result)


# 4. SOLUÇÃO DO PROBLEMA (Mochila com DP - Sem alterações)

def otimizar_orcamento(cursos_df: pd.DataFrame, orcamento: float):
    custos = cursos_df['custo'].tolist()
    impactos = cursos_df['impacto'].tolist()
    nomes = cursos_df['nome_curso'].tolist()
    n = len(custos)

    @lru_cache(None)
    def _resolver_mochila(orcamento_restante: float, indice_item: int) -> float:
        if indice_item < 0 or orcamento_restante <= 0:
            return 0
        custo_atual = custos[indice_item]
        impacto_atual = impactos[indice_item]

        if custo_atual > orcamento_restante:
            return _resolver_mochila(orcamento_restante, indice_item - 1)
        else:
            impacto_sem_incluir = _resolver_mochila(orcamento_restante, indice_item - 1)
            impacto_incluindo = impacto_atual + _resolver_mochila(
                orcamento_restante - custo_atual, 
                indice_item - 1
            )
            return max(impacto_sem_incluir, impacto_incluindo)

    def _rastrear_cursos(orcamento_total: float, n_total: int, max_impacto: float) -> list:
        cursos_selecionados = []
        orcamento_restante = orcamento_total
        for i in range(n_total - 1, -1, -1):
            valor_com_item_i = _resolver_mochila(orcamento_restante, i)
            valor_sem_item_i = _resolver_mochila(orcamento_restante, i - 1)
            
            if valor_com_item_i != valor_sem_item_i:
                curso = {
                    'nome': nomes[i],
                    'custo': custos[i],
                    'impacto': impactos[i]
                }
                cursos_selecionados.append(curso)
                orcamento_restante -= custos[i]
        return cursos_selecionados

    max_impacto = _resolver_mochila(orcamento, n - 1)
    cursos_escolhidos = _rastrear_cursos(orcamento, n, max_impacto)
    
    return max_impacto, cursos_escolhidos


# 5. ESTRUTURA DE SAÍDA

if __name__ == "__main__":
    print("=" * 60)
    print("      Executando o Otimizador de Treinamento 'UpSkill AI'      ")
    print("=" * 60)
    
    # DADOS DE ENTRADA
    engine = conectar_db()
    
    if engine is None:
        sys.exit("Falha na conexão. Encerrando o programa.") # Encerra o script

    # 1. Escolher o departamento
    df_deptos = buscar_departamentos(engine)
    if df_deptos.empty:
        sys.exit("Nenhum departamento encontrado no banco. Encerrando.")
        
    print("\nDepartamentos disponíveis:")
    print(df_deptos.to_string(index=False))
    
    try:
        id_depto_escolhido = int(input("\nDigite o ID do departamento para otimizar: "))
        depto_selecionado = df_deptos[df_deptos['id_depto'] == id_depto_escolhido]
        
        if depto_selecionado.empty:
            print("Erro: ID do departamento não encontrado.")
            sys.exit()
            
        # Pega o orçamento e o nome do departamento escolhido
        ORCAMENTO_DEPARTAMENTO = float(depto_selecionado['orcamento_treinamento'].iloc[0])
        NOME_DEPARTAMENTO = depto_selecionado['nome_depto'].iloc[0]
        
    except ValueError:
        print("Erro: ID inválido. Por favor, digite um número.")
        sys.exit()
    
    # 2. Buscar os cursos
    df_cursos = buscar_cursos(engine)
    if df_cursos.empty:
        sys.exit("Nenhum curso encontrado no banco. Encerrando.")

    print("\n" + "=" * 60)
    print(f"Otimizando para o Depto: {NOME_DEPARTAMENTO}")
    print(f"Total de cursos disponíveis na base: {len(df_cursos)}")
    print(f"Orçamento limite: R$ {ORCAMENTO_DEPARTAMENTO:,.2f}\n")
    
    # Demonstração da Ordenação
    print("--- Testando Função de Ordenação (Merge Sort por Custo) ---")
    df_ordenado_custo = merge_sort(df_cursos, 'custo')
    print(df_ordenado_custo[['nome_curso', 'custo']].head()) # Mostra os 5 mais baratos
    print("...\n")

    
    print("--- Calculando Otimização de Orçamento (Knapsack DP) ---")
    
    impacto_maximo, cursos_selecionados = otimizar_orcamento(
        df_cursos, 
        ORCAMENTO_DEPARTAMENTO
    )

    # Relatório Final
    print("\n" + "=" * 60)
    print("            RELATÓRIO DE OTIMIZAÇÃO FINAL            ")
    print("=" * 60)
    
    print(f"Departamento: {NOME_DEPARTAMENTO}")
    print(f"Orçamento Disponível: R$ {ORCAMENTO_DEPARTAMENTO:,.2f}")
    print(f"Impacto de Skill Maximizado: {impacto_maximo:,.0f} pontos\n")
    
    print("--- Cursos Recomendados ---")
    if not cursos_selecionados:
        print("Nenhum curso selecionado (Orçamento muito baixo ou lista vazia).")
    else:
        df_relatorio = pd.DataFrame(cursos_selecionados)
        df_relatorio = df_relatorio.sort_values(by='impacto', ascending=False)
        print(df_relatorio.to_string(index=False))
        
        print("-" * 60)
        custo_total = df_relatorio['custo'].sum()
        print(f"Custo Total: R$ {custo_total:,.2f}")
        print(f"Orçamento Restante: R$ {ORCAMENTO_DEPARTAMENTO - custo_total:,.2f}")

    print("=" * 60)