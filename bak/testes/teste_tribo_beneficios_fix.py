#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste da tribo Benefícios usando função fixa
===========================================
Este script testa se a tribo Benefícios está sendo analisada corretamente,
usando a função corrigida para análise de alocação.
"""

import os
import pandas as pd
import logging
import sys
import traceback
from fix_allocation import analisar_alocacao_fix

# Configurar logging mais detalhado
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        # Adicionar um arquivo de log também
        logging.FileHandler('teste_beneficios_fix.log')
    ]
)

def teste_tribo_beneficios_fix():
    """Testa análise da tribo Benefícios com função corrigida"""
    logging.info("Iniciando teste da tribo Benefícios com função corrigida...")
    
    try:
        # Importar as funções necessárias
        from agenteinsights.analise_insights import analisar_metricas_ageis, carregar_dados
        
        # Carregar dados via função padrão
        dados = carregar_dados()
        logging.info(f"Dados carregados. Tipos de dados: {type(dados)}")
        logging.info(f"Chaves no dicionário: {dados.keys() if isinstance(dados, dict) else 'Não é um dicionário'}")
        
        # Verificar se temos dados de alocação
        if 'alocacao' in dados and not dados['alocacao'].empty:
            df_alocacao = dados['alocacao']
            logging.info(f"Dados de alocação carregados: {len(df_alocacao)} registros")
            
            # Verificar tribos disponíveis
            tribos = df_alocacao['tribe'].unique()
            logging.info(f"Tribos disponíveis: {tribos}")
            
            # Verificar se a tribo Benefícios existe
            if 'Benefícios' in tribos:
                logging.info("Tribo Benefícios encontrada. Executando análise...")
                
                # 1. Testar análise de alocação usando função corrigida
                try:
                    resultado_alocacao = analisar_alocacao_fix(df_alocacao, tribo='Benefícios')
                    logging.info(f"Análise de alocação concluída: {len(resultado_alocacao['papeis'])} papéis encontrados")
                    
                    # Mostrar detalhes da análise
                    logging.info(f"Composição de squads: {list(resultado_alocacao['composicao_squads'].keys())}")
                    logging.info(f"Alocação média: {resultado_alocacao['alocacao_media']}")
                    logging.info(f"Média de pessoas por squad: {resultado_alocacao['media_pessoas_squad']}")
                    
                    # 2. Testar análise de métricas
                    try:
                        metricas = analisar_metricas_ageis(df_alocacao, tribo='Benefícios')
                        logging.info(f"Análise de métricas concluída: {metricas}")
                        
                        logging.info("Teste concluído com sucesso!")
                        return True
                        
                    except Exception as e:
                        logging.error(f"Erro na análise de métricas: {str(e)}")
                        traceback.print_exc()
                        return False
                        
                except Exception as e:
                    logging.error(f"Erro na análise de alocação: {str(e)}")
                    traceback.print_exc()
                    return False
            else:
                logging.error("Tribo Benefícios não encontrada nos dados")
                return False
        else:
            logging.error("Dados de alocação não disponíveis")
            return False
            
    except Exception as e:
        logging.error(f"Erro geral no teste: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    sucesso = teste_tribo_beneficios_fix()
    if sucesso:
        print("Teste concluído com sucesso!")
        sys.exit(0)
    else:
        print("Teste falhou")
        sys.exit(1)
