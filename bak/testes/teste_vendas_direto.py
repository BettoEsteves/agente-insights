"""
Teste simplificado da tribo Vendas
================================
Este script testa a função analisar_alocacao para a tribo Vendas,
com tratamento aprimorado para lidar com as normalizações.
"""

import os
import pandas as pd
import sys
import json
import traceback

try:
    # Importar as funções para análise
    from agenteinsights.analise_insights import analisar_alocacao, analisar_metricas_ageis
    
    print("\n==== Teste Direto da Tribo Vendas ====")
    try:
        # Carregar o arquivo diretamente
        base_dir = os.path.dirname(os.path.abspath(__file__))
        arquivo = os.path.join(base_dir, 'dados', 'Alocacao.xlsx')
        print(f"Carregando arquivo: {arquivo}")
        
        if os.path.exists(arquivo):
            df = pd.read_excel(arquivo)
            print(f"Arquivo carregado com sucesso. Quantidade: {len(df)} registros")
            print(f"Colunas disponíveis: {df.columns.tolist()}")
            
            # Verificar tribos disponíveis
            tribos = df['tribe'].unique().tolist()
            print(f"Tribos disponíveis: {tribos}")
            
            if 'Vendas' in tribos:
                print("\n1. Análise de alocação para Vendas")
                resultado_alocacao = analisar_alocacao(df, 'Vendas')
                print(f"✓ Análise de alocação concluída")
                print(f"  - Papéis encontrados: {list(resultado_alocacao['papeis'].keys())}")
                print(f"  - Squads encontrados: {list(resultado_alocacao['alocacao_media'].keys()) if resultado_alocacao['alocacao_media'] else 'Nenhum'}")
                print(f"  - Pessoas em múltiplos squads: {len(resultado_alocacao['pessoas_multi_squad'])}")
                
                print("\n2. Análise de métricas ágeis")
                try:
                    # Tentar análise de métricas sem padronizar_ids
                    metricas = analisar_metricas_ageis(df, tribo='Vendas')
                    print(f"✓ Métricas calculadas com sucesso: {json.dumps(metricas, indent=2)}")
                except Exception as e:
                    print(f"✗ Erro ao calcular métricas: {str(e)}")
                    traceback.print_exc()
            else:
                print(f"✗ Tribo Vendas não encontrada nas tribos disponíveis")
        else:
            print(f"✗ Arquivo não encontrado: {arquivo}")
    except Exception as e:
        print(f"✗ Erro ao carregar arquivo diretamente: {str(e)}")
        traceback.print_exc()
        
    print("\nTeste concluído!")
    
except ImportError as e:
    print(f"Erro de importação: {str(e)}")
    print("Verifique se o pacote agenteinsights está instalado corretamente")
    traceback.print_exc()
    sys.exit(1)
except Exception as e:
    print(f"Erro geral: {str(e)}")
    traceback.print_exc()
    sys.exit(1)
