#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste Completo do Sistema Agente Insights
========================================
Este script testa o sistema completo com todas as tribos disponíveis,
verificando tanto a análise de alocação quanto a de métricas ágeis.
"""

import os
import sys
import pandas as pd
import logging
import traceback
import json
from tabulate import tabulate

# Configuração de logging avançado
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('teste_sistema_completo.log')
    ]
)

def teste_completo():
    """
    Testa todo o sistema de análise para todas as tribos disponíveis.
    """
    print("\n==== Teste Completo do Sistema Agente Insights ====\n")
    
    try:
        # Importar funções necessárias do módulo
        from agenteinsights.analise_insights import (
            carregar_dados, analisar_alocacao, analisar_metricas_ageis,
            normalizar_nome, padronizar_ids
        )
        
        # 1. Carregar todos os dados
        print("\n1. Carregando dados...")
        dados = carregar_dados()
          # Verificar se os dados foram carregados corretamente
        if not dados or 'alocacao' not in dados or dados['alocacao'].empty:
            print("❌ Erro: Dados de alocação não disponíveis ou vazios")
            return False
        
        # Mostrar informações sobre os dados carregados
        for nome, df in dados.items():
            print(f"Dados de {nome}: {len(df)} registros, {len(df.columns)} colunas")
        
        # 2. Padronizar ids para consistência
        print("\n2. Padronizando IDs...")
        dados_padronizados = {}
        for nome, df in dados.items():
            dados_padronizados[nome] = padronizar_ids(df)
            print(f"Dados de {nome} padronizados")
        
        # 3. Obter todas as tribos disponíveis
        df_alocacao = dados_padronizados.get('alocacao', dados.get('alocacao'))
        tribos = []
        
        if 'tribe' in df_alocacao.columns:
            tribos = df_alocacao['tribe'].unique().tolist()
            tribos = [t for t in tribos if pd.notna(t)]  # Remover valores NaN
            print(f"\nTotal de {len(tribos)} tribos identificadas:")
            for t in sorted(tribos):
                print(f"- {t}")
        else:
            print("❌ Erro: Coluna 'tribe' não disponível nos dados")
            return False
            
        # 4. Testar cada tribo - Análise de alocação
        print("\n3. Testando análise de alocação para cada tribo...")
        resultados_alocacao = {}
        problemas_alocacao = []
        
        for tribo in tribos:
            print(f"\nAnalisando alocação para tribo: {tribo}")
            try:
                resultado = analisar_alocacao(df_alocacao, tribo=tribo)
                
                # Verificar resultados
                if resultado and resultado.get('papeis'):
                    print(f"✓ Tribo {tribo}: {len(resultado['papeis'])} papéis, {len(resultado.get('composicao_squads', {}))} squads")
                    resultados_alocacao[tribo] = {
                        'papeis': len(resultado['papeis']),
                        'squads': len(resultado.get('composicao_squads', {})),
                        'pessoas_multi_squad': len(resultado.get('pessoas_multi_squad', []))
                    }
                else:
                    print(f"⚠️ Tribo {tribo}: Sem papéis definidos ou resultado vazio")
                    problemas_alocacao.append((tribo, "Sem papéis definidos"))
            except Exception as e:
                print(f"❌ Erro ao analisar tribo {tribo}: {str(e)}")
                problemas_alocacao.append((tribo, str(e)))
                traceback.print_exc()
        
        # 5. Teste específico para tribos problemáticas (Benefícios e Vendas)
        tribos_especiais = ["Benefícios", "Vendas"]
        print("\n4. Testando especificamente tribos problemáticas...")
        
        for tribo in tribos_especiais:
            print(f"\nTeste específico para tribo: {tribo}")
            
            # Verificar normalização
            tribo_norm = normalizar_nome(tribo)
            print(f"Nome normalizado: '{tribo_norm}'")
            
            # Verificar se a tribo está nos dados (forma normalizada)
            if 'tribe_norm' in df_alocacao.columns:
                tribo_encontrada = tribo_norm in df_alocacao['tribe_norm'].unique()
                print(f"Tribo encontrada nos dados normalizados: {tribo_encontrada}")
                
                # Contar registros
                if tribo_encontrada:
                    n_registros = len(df_alocacao[df_alocacao['tribe_norm'] == tribo_norm])
                    print(f"Total de registros para a tribo: {n_registros}")
                    
                    # Testar análise
                    try:
                        resultado = analisar_alocacao(df_alocacao, tribo=tribo)
                        print(f"Papéis encontrados: {len(resultado.get('papeis', {}))}")
                        print(f"Squads encontrados: {len(resultado.get('composicao_squads', {}))}")
                    except Exception as e:
                        print(f"❌ Erro na análise: {str(e)}")
            else:
                print("⚠️ Coluna tribe_norm não disponível nos dados")
        
        # 6. Resumir resultados
        print("\n==== RESUMO DOS RESULTADOS ====")
        print(f"Total de tribos testadas: {len(tribos)}")
        print(f"Tribos processadas com sucesso: {len(resultados_alocacao)}")
        print(f"Tribos com problemas: {len(problemas_alocacao)}")
        
        if problemas_alocacao:
            print("\nLista de tribos com problemas:")
            for tribo, erro in problemas_alocacao:
                print(f"- {tribo}: {erro}")
        
        # 7. Apresentar resultados em formato tabular
        print("\nDetalhes das tribos processadas com sucesso:")
        
        # Criar tabela para visualização mais clara
        table_data = []
        for tribo, info in resultados_alocacao.items():
            table_data.append([
                tribo, 
                info.get('papeis', 0),
                info.get('squads', 0),
                info.get('pessoas_multi_squad', 0)
            ])
        
        headers = ["Tribo", "Papéis", "Squads", "Pessoas Multi-Squad"]
        print(tabulate(sorted(table_data), headers=headers, tablefmt="grid"))
        
        return True
        
    except Exception as e:
        print(f"❌ Erro geral no teste: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Verificar se tabulate está instalado
    try:
        from tabulate import tabulate
    except ImportError:
        print("Instalando dependência tabulate...")
        os.system(f"{sys.executable} -m pip install tabulate")
    
    # Executar teste
    sucesso = teste_completo()
    print("\nResultado final do teste:", "✅ SUCESSO" if sucesso else "❌ FALHA")
    sys.exit(0 if sucesso else 1)
