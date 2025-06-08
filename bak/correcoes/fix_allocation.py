#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Fix para o problema da análise de alocação
=========================================
Este script corrige o problema com a análise de alocação,
considerando diferentes nomes para a coluna de percentual de alocação.
"""

import pandas as pd
import logging
from collections import Counter
from typing import Dict

def analisar_alocacao_fix(dados: pd.DataFrame, tribo: str = None, squad: str = None) -> Dict:
    """Versão corrigida da função que analisa alocação de pessoas e papéis"""
    try:
        # Criar cópia dos dados
        df = dados.copy() if not dados.empty else pd.DataFrame()
        
        # Verificar colunas necessárias
        colunas_necessarias = ['endDate', 'role', 'squad', 'tribe', 'person']
        
        # Verificar variações da coluna de alocação percentual
        coluna_percentual = None
        for possivel_coluna in ['percentageAllocation', 'percetageAllocation', 'percentage', 'alocacao_percentual']:
            if possivel_coluna in df.columns:
                coluna_percentual = possivel_coluna
                logging.info(f"Coluna de percentual de alocação encontrada: {possivel_coluna}")
                break
                
        if not all(col in df.columns for col in colunas_necessarias):
            missing_cols = [col for col in colunas_necessarias if col not in df.columns]
            logging.warning(f"Colunas ausentes para análise de alocação: {missing_cols}")
            return {
                'papeis': {},
                'alocacao_media': {},
                'pessoas_multi_squad': [],
                'composicao_squads': {},
                'media_pessoas_squad': 0
            }
        
        # Filtrar apenas alocações ativas (sem data de término ou data futura)
        df = df[df['endDate'].isna() | (pd.to_datetime(df['endDate'], errors='coerce') > pd.Timestamp.now())]
        
        if tribo:
            df = df[df['tribe'] == tribo]
        if squad:
            df = df[df['squad'] == squad]
            
        # Verificar se o DataFrame ficou vazio após filtros
        if df.empty:
            return {
                'papeis': {},
                'alocacao_media': {},
                'pessoas_multi_squad': [],
                'composicao_squads': {},
                'media_pessoas_squad': 0
            }
        
        # Calcular papéis
        papeis = df.groupby('role').size().to_dict() if 'role' in df.columns else {}
        
        # Calcular pessoas em múltiplos squads
        try:
            pessoas_multi_squad = df[df.groupby('person')['squad'].transform('size') > 1]['person'].unique().tolist() if 'person' in df.columns and 'squad' in df.columns else []
        except Exception as e:
            logging.warning(f"Erro ao calcular pessoas em múltiplos squads: {str(e)}")
            pessoas_multi_squad = []
        
        # Calcular média de pessoas por squad
        try:
            media_pessoas_squad = float(df.groupby('squad')['person'].nunique().mean()) if 'squad' in df.columns and 'person' in df.columns else 0
        except Exception as e:
            logging.warning(f"Erro ao calcular média de pessoas por squad: {str(e)}")
            media_pessoas_squad = 0
        
        # Preparar resposta
        analise = {
            'papeis': papeis,
            'pessoas_multi_squad': pessoas_multi_squad,
            'media_pessoas_squad': media_pessoas_squad,
            'alocacao_media': {},
            'composicao_squads': {}
        }
        
        # Adicionar informações de percentual se a coluna for encontrada
        if coluna_percentual:
            try:
                # Verificar se a coluna de percentual é numérica
                if not pd.api.types.is_numeric_dtype(df[coluna_percentual]):
                    logging.info(f"Processando coluna {coluna_percentual}")
                    # Mostrar amostras dos valores antes da conversão
                    amostra = df[coluna_percentual].dropna().head(5).tolist()
                    logging.info(f"Amostras de valores antes da conversão: {amostra}")
                    
                    # Limpar valores (remover % e outros caracteres)
                    df[coluna_percentual] = df[coluna_percentual].astype(str).str.replace('%', '').str.replace(',', '.').str.strip()
                    
                    # Mostrar valores após limpeza
                    amostra_limpa = df[coluna_percentual].dropna().sample(min(3, len(df))).tolist()
                    logging.info(f"Valores após limpeza: {amostra_limpa}")
                    
                    # Converter para float
                    df[coluna_percentual] = pd.to_numeric(df[coluna_percentual], errors='coerce')
                    
                    # Verificar o range dos valores e normalizar se necessário (0-100 -> 0-1)
                    if df[coluna_percentual].max() > 1:
                        min_val = df[coluna_percentual].min()
                        max_val = df[coluna_percentual].max()
                        mean_val = df[coluna_percentual].mean()
                        logging.info(f"Valores de percentual: min={min_val}, max={max_val}, mean={mean_val}")
                        
                        # Converter para escala 0-1 se estiver na escala 0-100
                        logging.info("Convertendo percentuais para decimal (0-1)")
                        df[coluna_percentual] = df[coluna_percentual] / 100
                        
                        # Log após conversão
                        min_val = df[coluna_percentual].min()
                        max_val = df[coluna_percentual].max()
                        mean_val = df[coluna_percentual].mean()
                        logging.info(f"Valores após normalização: min={min_val}, max={max_val}, mean={mean_val}")
                
                # Calcular média de alocação por squad
                alocacao_media = df.groupby('squad')[coluna_percentual].mean().to_dict()
                analise['alocacao_media'] = alocacao_media
                
                # Composição de squads com informações de papéis e percentual médio
                composicao_squads = {}
                for squad_name, squad_df in df.groupby('squad'):
                    composicao_squads[squad_name] = {
                        'papeis': Counter(squad_df['role']),
                        'percentual_medio': float(squad_df[coluna_percentual].mean())
                    }
                analise['composicao_squads'] = composicao_squads
                
            except Exception as e:
                logging.error(f"Erro ao processar coluna de percentual: {str(e)}")
                # Não quebramos a análise por erro no percentual
        else:
            # Composição de squads só com informações de papéis
            composicao_squads = {}
            for squad_name, squad_df in df.groupby('squad'):
                composicao_squads[squad_name] = {
                    'papeis': Counter(squad_df['role'])
                }
            analise['composicao_squads'] = composicao_squads
        
        return analise
        
    except Exception as e:
        logging.error(f"Erro ao analisar alocação: {str(e)}")
        return {
            'papeis': {},
            'alocacao_media': {},
            'pessoas_multi_squad': [],
            'composicao_squads': {},
            'media_pessoas_squad': 0
        }

# Teste rápido da função
if __name__ == "__main__":
    print("Este script contém apenas a função corrigida para análise de alocação.")
    print("Execute o teste_tribo_beneficios.py para testar a função.")
