
import pandas as pd
import logging
from typing import Tuple

def cruzar_dados(maturidade: pd.DataFrame,
                 alocacao: pd.DataFrame,
                 executivo: pd.DataFrame) -> pd.DataFrame:
    """
    Cruza os dados entre os DataFrames de maturidade, alocação e executivo.
    
    Args:
        maturidade: DataFrame com dados de maturidade das tribos
        alocacao: DataFrame com dados de alocação
        executivo: DataFrame com dados executivos
        
    Returns:
        DataFrame com os dados cruzados
        
    Raises:
        ValueError: Se alguma coluna necessária estiver faltando
    """
    try:
        # Validar colunas necessárias
        colunas_necessarias = {
            'maturidade': ['Tribo'],
            'alocacao': ['endDate', 'tribe', 'squadID', 'tribeID'],
            'executivo': ['PBI_Concuidos_Executivo[ID_Squad]', 
                         'PBI_Concuidos_Executivo[ID_Tribo]']
        }
        
        for df, colunas in [
            (maturidade, colunas_necessarias['maturidade']),
            (alocacao, colunas_necessarias['alocacao']),
            (executivo, colunas_necessarias['executivo'])
        ]:
            colunas_faltantes = [col for col in colunas if col not in df.columns]
            if colunas_faltantes:
                raise ValueError(f"Colunas faltantes: {colunas_faltantes}")
        
        # Filtrar alocações ativas (sem endDate)
        logging.info("Filtrando alocações ativas...")
        alocacao_ativa = alocacao[alocacao['endDate'].isna()].copy()
        
        # Merge entre MaturidadeT e Alocacao
        logging.info("Realizando merge entre Maturidade e Alocação...")
        merged_df = pd.merge(
            maturidade,
            alocacao_ativa,
            left_on='Tribo',
            right_on='tribe',
            how='inner'
        )
        
        # Merge entre o resultado anterior e Executivo
        logging.info("Realizando merge com dados Executivos...")
        merged_df = pd.merge(
            merged_df,
            executivo,
            left_on=['squadID', 'tribeID'],
            right_on=['PBI_Concuidos_Executivo[ID_Squad]',
                     'PBI_Concuidos_Executivo[ID_Tribo]'],
            how='inner'
        )
        
        # Verificar se há dados após os merges
        if merged_df.empty:
            logging.warning("Nenhum dado encontrado após o cruzamento")
        else:
            logging.info(f"Cruzamento concluído com {len(merged_df)} registros")
        
        return merged_df
        
    except Exception as e:
        logging.error(f"Erro ao cruzar dados: {str(e)}")
        raise
