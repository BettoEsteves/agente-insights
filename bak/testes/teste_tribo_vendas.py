"""
Teste de Análise da Tribo Vendas
================================
Script para testar se a tribo Vendas está sendo analisada corretamente.
"""

import os
import sys
import pandas as pd
import logging
import traceback
from pathlib import Path

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,  # Mudado para DEBUG para mais detalhes
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('teste_tribo_vendas.log'),
        logging.StreamHandler()
    ]
)

# Adicionar diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
logging.info(f"Python path: {sys.path}")

try:
    from agenteinsights.analise_insights import carregar_dados, analisar_metricas_ageis
    logging.info("Módulos importados com sucesso!")
except ImportError as e:
    logging.error(f"Erro ao importar módulos: {str(e)}")
    traceback.print_exc()

def teste_tribo_vendas():
    logging.info("Iniciando teste da tribo Vendas...")
    
    try:
        # Carregar dados
        dados = carregar_dados()
        logging.debug(f"Tipo de retorno de carregar_dados: {type(dados)}")
        logging.debug(f"Chaves no dicionário: {dados.keys() if isinstance(dados, dict) else 'Não é um dicionário'}")
        
        # Verificar tribos disponíveis
        df_alocacao = dados.get('alocacao', pd.DataFrame())
        logging.debug(f"DataFrame alocacao: {df_alocacao.shape} registros")
        logging.debug(f"Colunas alocacao: {df_alocacao.columns.tolist() if not df_alocacao.empty else 'DataFrame vazio'}")
        
        if not df_alocacao.empty:
            tribos = df_alocacao['tribe'].unique()
            logging.info(f"Tribos disponíveis: {tribos}")
            
            # Normalizar os nomes para comparação case insensitive
            tribos_norm = [str(t).strip().lower() for t in tribos if pd.notna(t)]
            logging.debug(f"Tribos normalizadas: {tribos_norm}")
            
            # Verificar se a tribo Vendas existe (case insensitive)
            if any('vendas' in t for t in tribos_norm):
                # Encontrar o nome exato da tribo no caso original
                tribo_vendas = next((t for t in tribos if 'vendas' in str(t).lower()), None)
                logging.info(f"Tribo Vendas encontrada como '{tribo_vendas}'. Executando análise...")
                
                # Testar análise de métricas para a tribo Vendas
                try:
                    # Se dados_cruzados não estiver disponível, usar alocacao
                    df_analise = dados.get('dados_cruzados', df_alocacao)
                      # Normalizar nomes de tribos para comparação
                    if 'tribe_norm' not in df_analise.columns:
                        from agenteinsights.analise_insights import analisar_alocacao
                        # Em vez de usar padronizar_ids, usamos analisar_alocacao para a tribo
                        try:
                            resultado = analisar_alocacao(df_analise, tribo=tribo_vendas)
                            logging.debug(f"Análise de alocação: {resultado}")
                        except Exception as e:
                            logging.error(f"Erro ao analisar alocação: {str(e)}")
                            traceback.print_exc()
                    
                    metricas = analisar_metricas_ageis(df_analise, tribo=tribo_vendas)
                    logging.info(f"Métricas da Tribo Vendas: {metricas}")
                    return True
                except Exception as e:
                    logging.error(f"Erro ao analisar tribo Vendas: {str(e)}")
                    traceback.print_exc()
                    return False
            else:
                logging.warning("Tribo Vendas não encontrada nos dados.")
                return False
        else:
            logging.error("Dados de alocação vazios ou não carregados.")
            return False
            
    except Exception as e:
        logging.error(f"Erro geral no teste: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    resultado = teste_tribo_vendas()
    print(f"Teste concluído: {'Sucesso' if resultado else 'Falha'}")
