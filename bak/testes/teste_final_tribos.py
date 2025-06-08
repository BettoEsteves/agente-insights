"""
Teste final para todas as tribos
================================
Este script testa a análise para todas as tribos disponíveis,
verificando se todas são processadas corretamente com os ajustes realizados.
"""

import os
import pandas as pd
import sys
import traceback
import json
from datetime import datetime
import logging

# Configurar logging básico
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# Evitar caracteres Unicode no logging para evitar problemas com codificação
def log_info(message):
    try:
        logging.info(message)
    except UnicodeEncodeError:
        logging.info("Mensagem contém caracteres especiais (log omitido)")

def testar_todas_tribos():
    """Testa a análise para todas as tribos disponíveis"""
    print(f"=== TESTE DE TODAS AS TRIBOS ===")
    print(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"===========================\n")
    
    try:
        # Importar funções necessárias
        from agenteinsights.analise_insights import analisar_alocacao, analisar_metricas_ageis, carregar_dados
        print("1. Funções importadas com sucesso.")
        
        # Carregar dados
        dados = carregar_dados()
        print(f"2. Dados carregados com sucesso. Tipos: {type(dados)}")
        
        # Verificar dataset de alocação
        if 'alocacao' not in dados or dados['alocacao'].empty:
            print("ERRO: Dados de alocação não encontrados ou vazios.")
            return False
            
        df_alocacao = dados['alocacao']
        print(f"3. Dataset de alocação: {len(df_alocacao)} registros")
        
        # Obter todas as tribos
        tribos = df_alocacao['tribe'].unique().tolist()
        print(f"4. Total de {len(tribos)} tribos encontradas.")
        
        # Preparar resultados
        resultados = {
            "total_tribos": len(tribos),
            "sucessos": 0,
            "falhas": 0,
            "detalhes": {}
        }
        
        # Testar cada tribo
        for idx, tribo in enumerate(sorted(tribos)):
            print(f"\n--- Testando tribo {idx+1}/{len(tribos)}: {tribo} ---")
            try:
                # 1. Análise de alocação
                resultado_alocacao = analisar_alocacao(df_alocacao, tribo=tribo)
                papeis = len(resultado_alocacao['papeis']) if resultado_alocacao and 'papeis' in resultado_alocacao else 0
                squads = len(resultado_alocacao['alocacao_media']) if resultado_alocacao and 'alocacao_media' in resultado_alocacao else 0
                
                # 2. Análise de métricas
                metricas = analisar_metricas_ageis(df_alocacao, tribo=tribo)
                
                # Registrar sucesso
                print(f"[SUCESSO] Tribo {tribo}: {papeis} papéis, {squads} squads")
                resultados["sucessos"] += 1
                resultados["detalhes"][tribo] = {
                    "status": "sucesso",
                    "papeis": papeis,
                    "squads": squads
                }
            except Exception as e:
                # Registrar falha
                print(f"[FALHA] Tribo {tribo}: {str(e)}")
                traceback.print_exc()
                resultados["falhas"] += 1
                resultados["detalhes"][tribo] = {
                    "status": "falha",
                    "erro": str(e)
                }
        
        # Imprimir resumo
        print("\n=== RESUMO DO TESTE ===")
        print(f"Total de tribos: {resultados['total_tribos']}")
        print(f"Sucessos: {resultados['sucessos']}")
        print(f"Falhas: {resultados['falhas']}")
        
        # Salvar resultados em arquivo JSON
        with open('resultado_teste_tribos.json', 'w', encoding='utf-8') as f:
            json.dump(resultados, f, ensure_ascii=False, indent=2)
        print("Resultados detalhados salvos em 'resultado_teste_tribos.json'")
        
        return resultados["falhas"] == 0
        
    except Exception as e:
        print(f"ERRO GERAL: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    sucesso = testar_todas_tribos()
    if sucesso:
        print("\nTODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
        sys.exit(0)
    else:
        print("\nTESTES CONCLUÍDOS COM FALHAS!")
        sys.exit(1)
