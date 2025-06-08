"""
Agente Insights - Módulo de Análise ML
=====================================
Versão: 1.4.2
Release: 3
Data: 01/06/2025

Histórico:
- 1.0.0 (Release 0): Versão inicial
- 1.1.0 (Release 2): Correção no processamento de DataFrames
- 1.2.0 (Release 2): Implementada seleção dinâmica de colunas para análise
- 1.3.0 (Release 2): Melhorado tratamento de colunas categóricas
- 1.4.0 (Release 3): Implementada detecção inteligente de colunas numéricas
- 1.4.1 (Release 3): Corrigido problema de indentação no código
- 1.4.2 (Release 3): Melhorado tratamento de tipos de dados

Descrição:
Módulo responsável pela execução das análises de machine learning,
incluindo regressão linear, clustering e análises estatísticas.
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import logging
import re
from typing import Dict, Any, List, Optional

def is_numeric_column(series: pd.Series) -> bool:
    """Verifica se uma coluna é numérica e adequada para análise."""
    try:
        # Remove valores nulos
        non_null = series.dropna()
        if len(non_null) == 0:
            return False
            
        # Verifica o tipo da coluna
        if pd.api.types.is_datetime64_any_dtype(series):
            return False
            
        if pd.api.types.is_bool_dtype(series):
            return False
            
        # Verifica se parece ser uma coluna de ID
        if series.dtype == 'object':
            # Se mais de 80% dos valores são strings que parecem IDs, retorna False
            id_pattern = re.compile(r'^[A-Z0-9]+$')
            id_like = series.str.match(id_pattern).mean() > 0.8
            if id_like:
                return False
                
        # Tenta converter para número
        numeric_series = pd.to_numeric(non_null, errors='coerce')
        # Verifica se há valores numéricos suficientes
        if numeric_series.isna().mean() > 0.5:  # Se mais de 50% são NaN
            return False
        return True
    except:
        return False

def get_numeric_columns(df: pd.DataFrame) -> List[str]:
    """Retorna lista de colunas numéricas válidas para análise."""
    numeric_cols = []
    for col in df.columns:
        if is_numeric_column(df[col]):
            numeric_cols.append(col)
            logging.info(f"Coluna {col} identificada como numérica")
        else:
            logging.info(f"Coluna {col} ignorada (não numérica ou inadequada para análise)")
    return numeric_cols

def executar_analises(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Executa análises de ML no DataFrame fornecido.
    
    Args:
        df: DataFrame com os dados para análise
        
    Returns:
        Dicionário com resultados das análises
    """
    logging.info(f"Iniciando análises para DataFrame com {len(df)} linhas")
    
    # Identificar colunas numéricas
    colunas_analise = get_numeric_columns(df)
    logging.info(f"Colunas numéricas identificadas: {colunas_analise}")
    
    if len(colunas_analise) < 2:
        logging.warning("Dados insuficientes para análise")
        return {
            'status': 'error',
            'message': 'Dados insuficientes para análise',
            'regressao': None,
            'clustering': None,
            'estatisticas': None
        }
    
    try:
        # Preparar dados
        X = df[colunas_analise].fillna(df[colunas_analise].mean())
        
        # Padronizar dados
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Regressão Linear
        reg = LinearRegression()
        y = X_scaled[:, 0]  # primeira coluna como target
        X_reg = X_scaled[:, 1:]  # demais colunas como features
        reg.fit(X_reg, y)
        
        # Clustering
        kmeans = KMeans(n_clusters=3, random_state=42)
        clusters = kmeans.fit_predict(X_scaled)
        
        # Estatísticas descritivas
        estatisticas = df[colunas_analise].describe()
        
        return {
            'status': 'success',
            'regressao': {
                'coef': reg.coef_.tolist(),
                'intercept': float(reg.intercept_),
                'r2': reg.score(X_reg, y)
            },
            'clustering': {
                'labels': clusters.tolist(),
                'centroids': kmeans.cluster_centers_.tolist(),
                'inertia': float(kmeans.inertia_)
            },
            'estatisticas': estatisticas.to_dict()
        }
        
    except Exception as e:
        logging.error(f"Erro durante análises: {str(e)}")
        raise
