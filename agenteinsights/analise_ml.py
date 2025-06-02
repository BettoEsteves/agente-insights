"""
Agente Insights - Módulo de Análise ML
=====================================
Versão: 1.4.0
Release: 5
Data: 01/06/2025

Histórico:
- 1.0.0 (Release 0): Versão inicial
- 1.1.0 (Release 2): Correção no processamento de DataFrames
- 1.2.0 (Release 3): Implementada seleção dinâmica de colunas para análise
- 1.3.0 (Release 4): Melhorado tratamento de colunas categóricas e valores não numéricos
- 1.4.0 (Release 5): Implementada detecção inteligente de colunas numéricas e tratamento avançado de dados

Descrição:
Módulo responsável pela execução das análises de machine learning,
incluindo regressão linear, clustering e análises estatísticas.
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import os
import logging
from typing import Dict, Any
from pathlib import Path

# Criar diretórios necessários
def criar_diretorios() -> None:
    """Cria os diretórios necessários para o funcionamento do script."""
    diretorios = [
        'output',
        'output/logs',
        'output/modelos',
        'output/graficos',
        'output/relatorios'
    ]
    for diretorio in diretorios:
        Path(diretorio).mkdir(parents=True, exist_ok=True)

# Criar diretórios antes de configurar logging
criar_diretorios()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='output/logs/analise_ml.log',
    encoding='utf-8'
)

def executar_analises(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Executa análises de machine learning nos dados fornecidos.
    
    Args:
        df: DataFrame com os dados para análise
        
    Returns:
        Dict com os resultados das análises
    """
    try:
        resultados = {}
        
        # Análise Descritiva
        logging.info("Iniciando análise descritiva...")
        resultados['descritiva'] = df.describe()
        
        # Verificar e tratar valores ausentes
        if df.isnull().any().any():
            logging.warning("Detectados valores ausentes nos dados")
            df = df.fillna(df.mean())        # Análise Preditiva (Regressão Linear)
        logging.info("Iniciando análise preditiva...")
        
        # Seleção dinâmica de colunas numéricas para análise
        colunas_numericas = df.select_dtypes(include=['int64', 'float64']).columns
        colunas_categoricas = df.select_dtypes(include=['object']).columns
        
        # Logging de informações sobre as colunas
        logging.info(f"Colunas numéricas encontradas: {colunas_numericas.tolist()}")
        logging.info(f"Colunas categóricas encontradas: {colunas_categoricas.tolist()}")
        
        if len(colunas_numericas) < 2:
            logging.warning("Insuficientes colunas numéricas para análise")
            resultados['preditiva'] = None
            return resultados
        
        # Preparar dados para análise
        logging.info(f"Colunas disponíveis: {df.columns.tolist()}")
        
        # Identificar colunas para análise
        colunas_analise = []
        for col in df.columns:
            try:
                # Tentar converter para numérico
                valores = pd.to_numeric(df[col], errors='coerce')
                # Se mais de 50% dos valores são numéricos válidos, usar a coluna
                if valores.notna().sum() > len(df) * 0.5:
                    colunas_analise.append(col)
                    df[col] = valores
            except:
                continue
        
        if len(colunas_analise) < 2:
            logging.warning(f"Insuficientes colunas numéricas para análise. Encontradas: {colunas_analise}")
            resultados['preditiva'] = None
            return resultados
        
        logging.info(f"Usando colunas para análise: {colunas_analise}")
        
        # Preparar dados para análise
        df_analise = df[colunas_analise].copy()
        
        # Tratar valores ausentes
        for col in df_analise.columns:
            if df_analise[col].isnull().any():
                df_analise[col] = df_analise[col].fillna(df_analise[col].mean())
        
        # Usar todas as colunas exceto a última como features
        X = df_analise[colunas_analise[:-1]]
        y = df_analise[colunas_analise[-1]]
        
        logging.info(f"Usando colunas para análise: {X.columns.tolist()}")
        
        # Padronizar os dados
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        modelo_regressao = LinearRegression()
        modelo_regressao.fit(X_scaled, y)
        resultados['regressao'] = {
            'coeficientes': dict(zip(X.columns, modelo_regressao.coef_)),
            'r2': modelo_regressao.score(X_scaled, y)
        }
        
        # Análise Prescritiva (Clustering com KMeans)
        logging.info("Iniciando análise prescritiva...")
        kmeans = KMeans(n_clusters=3, random_state=42)
        df['cluster'] = kmeans.fit_predict(X_scaled)
        resultados['clusters'] = {
            'centros': kmeans.cluster_centers_,
            'inertia': kmeans.inertia_
        }
        
        # Análise Diagnóstica (Correlação)
        logging.info("Iniciando análise diagnóstica...")
        correlacao = df.corr()
        resultados['correlacao'] = correlacao
        
        # Salvar gráficos
        logging.info("Gerando visualizações...")
        plt.style.use('seaborn')
        
        # Heatmap de correlação
        plt.figure(figsize=(12, 10))
        sns.heatmap(correlacao, annot=True, cmap='coolwarm', fmt='.2f')
        plt.title('Heatmap de Correlação entre Variáveis')
        plt.tight_layout()
        plt.savefig('output/graficos/correlacao_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Gráfico de clusters
        plt.figure(figsize=(12, 8))
        scatter = sns.scatterplot(
            data=df,
            x='SumStory_Points',
            y='Maturidade',
            hue='cluster',
            palette='deep',
            size='SumHoras_Capex',
            sizes=(50, 400),
            alpha=0.6
        )
        plt.title('Clusters de Maturidade vs. Story Points')
        plt.legend(title='Cluster', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.savefig('output/graficos/clusters_scatterplot.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Salvar modelos
        logging.info("Salvando modelos...")
        with open('output/modelos/modelo_regressao.pkl', 'wb') as f:
            pickle.dump({
                'modelo': modelo_regressao,
                'scaler': scaler
            }, f)
        
        with open('output/modelos/modelo_kmeans.pkl', 'wb') as f:
            pickle.dump({
                'modelo': kmeans,
                'scaler': scaler
            }, f)
        
        logging.info("Análise concluída com sucesso!")
        return resultados
        
    except Exception as e:
        logging.error(f"Erro durante a execução das análises: {str(e)}")
        raise
