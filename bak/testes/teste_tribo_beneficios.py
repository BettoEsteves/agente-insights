"""
Teste da tribo Benefícios
=======================
Este script testa se a tribo Benefícios está sendo analisada corretamente,
usando os códigos já corrigidos.
"""

import os
import pandas as pd
import logging
import sys
import traceback

# Configurar logging mais detalhado
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        # Adicionar um arquivo de log também
        logging.FileHandler('teste_beneficios.log')
    ]
)

def teste_tribo_beneficios():
    """Testa análise da tribo Benefícios"""
    logging.info("Iniciando teste da tribo Benefícios...")
    
    try:
        # Importar as funções necessárias
        from agenteinsights.analise_insights import analisar_alocacao, analisar_metricas_ageis, carregar_dados
        
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
                
                # 1. Testar análise de alocação
                try:
                    resultado_alocacao = analisar_alocacao(df_alocacao, tribo='Benefícios')
                    logging.info(f"✓ Análise de alocação concluída: {len(resultado_alocacao['papeis'])} papéis encontrados")
                    
                    # 2. Testar análise de métricas
                    try:
                        metricas = analisar_metricas_ageis(df_alocacao, tribo='Benefícios')
                        logging.info(f"✓ Análise de métricas concluída: {metricas}")
                        
                        logging.info("✅ Teste concluído com sucesso!")
                        return True
                        
                    except Exception as e:
                        logging.error(f"❌ Erro na análise de métricas: {str(e)}")
                        traceback.print_exc()
                        return False
                        
                except Exception as e:
                    logging.error(f"❌ Erro na análise de alocação: {str(e)}")
                    traceback.print_exc()
                    return False
            else:
                logging.error("❌ Tribo Benefícios não encontrada nos dados")
                return False
        else:
            logging.error("❌ Dados de alocação não disponíveis")
            return False
            
    except Exception as e:
        logging.error(f"❌ Erro geral no teste: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    sucesso = teste_tribo_beneficios()
    if sucesso:
        print("✅ Teste concluído com sucesso!")
        sys.exit(0)
    else:
        print("❌ Teste falhou")
        sys.exit(1)
