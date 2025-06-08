#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste Específico para Tribos Problemáticas
=========================================
Este script testa especificamente as tribos Benefícios e Vendas
que apresentavam problemas anteriormente.
"""

import os
import sys
import pandas as pd
import logging
import traceback
import json

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('teste_tribos_especificas.log')
    ]
)

def testar_tribos_especificas():
    """
    Testa especificamente as tribos Benefícios e Vendas.
    """
    print("\n==== Teste Específico para Tribos Problemáticas ====\n")
    
    # Lista de tribos a serem testadas
    tribos_especiais = ["Benefícios", "Vendas"]
    
    try:
        # Importar funções necessárias
        from agenteinsights.analise_insights import (
            carregar_dados, analisar_alocacao, analisar_metricas_ageis,
            normalizar_nome
        )
        
        # 1. Carregar dados
        print("1. Carregando dados...")
        dados = carregar_dados()
        
        if not dados or not dados.get('alocacao') or dados['alocacao'].empty:
            print("❌ Erro: Dados de alocação não disponíveis")
            return False
            
        df_alocacao = dados['alocacao']
        print(f"Dados carregados: {len(df_alocacao)} registros")
        print(f"Colunas disponíveis: {df_alocacao.columns.tolist()}")
        
        # 2. Verificar se há coluna tribe_norm, caso contrário, criá-la
        if 'tribe_norm' not in df_alocacao.columns:
            print("Criando coluna tribe_norm...")
            df_alocacao['tribe_norm'] = df_alocacao['tribe'].apply(normalizar_nome)
        
        # 3. Testar cada tribo especial
        resultados = {}
        
        for tribo in tribos_especiais:
            print(f"\n==== Testando tribo: {tribo} ====")
            
            # Normalizar o nome da tribo
            tribo_norm = normalizar_nome(tribo)
            print(f"Nome normalizado: '{tribo_norm}'")
            
            # Verificar se a tribo existe nos dados (original e normalizada)
            tribo_encontrada_original = tribo in df_alocacao['tribe'].unique()
            tribo_encontrada_norm = tribo_norm in df_alocacao['tribe_norm'].unique()
            
            print(f"Tribo encontrada (busca original): {tribo_encontrada_original}")
            print(f"Tribo encontrada (busca normalizada): {tribo_encontrada_norm}")
            
            # Contar registros
            registros_original = len(df_alocacao[df_alocacao['tribe'] == tribo])
            registros_norm = len(df_alocacao[df_alocacao['tribe_norm'] == tribo_norm])
            
            print(f"Registros (busca original): {registros_original}")
            print(f"Registros (busca normalizada): {registros_norm}")
            
            # Mostrar amostra dos registros para debug
            if registros_norm > 0:
                amostra = df_alocacao[df_alocacao['tribe_norm'] == tribo_norm].head(3)
                print("\nAmostra de registros:")
                for idx, row in amostra.iterrows():
                    print(f"  - Pessoa: {row.get('person')}, Squad: {row.get('squad')}, Papel: {row.get('role')}")
            
            # 4. Executar análise para cada tribo
            print("\nExecutando análise de alocação...")
            try:
                resultado = analisar_alocacao(df_alocacao, tribo=tribo)
                
                if resultado and resultado.get('papeis'):
                    print(f"✅ Análise bem-sucedida:")
                    print(f"  - Papéis encontrados: {len(resultado['papeis'])}")
                    print(f"  - Squads: {len(resultado.get('composicao_squads', {}))}")
                    print(f"  - Pessoas em múltiplos squads: {len(resultado.get('pessoas_multi_squad', []))}")
                    
                    # Mostrar papéis encontrados
                    print("\nPapéis encontrados:")
                    for papel, qtd in resultado['papeis'].items():
                        print(f"  - {papel}: {qtd}")
                    
                    resultados[tribo] = {
                        'sucesso': True,
                        'papeis': len(resultado['papeis']),
                        'squads': len(resultado.get('composicao_squads', {})),
                        'pessoas_multi_squad': len(resultado.get('pessoas_multi_squad', []))
                    }
                    
                else:
                    print(f"⚠️ Análise concluída, mas sem papéis definidos")
                    resultados[tribo] = {
                        'sucesso': False,
                        'erro': "Sem papéis definidos"
                    }
                    
            except Exception as e:
                print(f"❌ Erro na análise: {str(e)}")
                traceback.print_exc()
                resultados[tribo] = {
                    'sucesso': False,
                    'erro': str(e)
                }
        
        # 5. Resultado final
        print("\n==== Resumo dos Resultados ====")
        sucesso_total = all(r.get('sucesso', False) for r in resultados.values())
        
        print(f"Tribos testadas: {len(tribos_especiais)}")
        print(f"Resultado final: {'✅ SUCESSO' if sucesso_total else '❌ FALHA'}")
        
        for tribo, res in resultados.items():
            status = "✅ OK" if res.get('sucesso') else "❌ Falha"
            detalhes = f"{res.get('papeis', 0)} papéis, {res.get('squads', 0)} squads" if res.get('sucesso') else res.get('erro')
            print(f"- {tribo}: {status} - {detalhes}")
        
        return sucesso_total
        
    except Exception as e:
        print(f"❌ Erro geral no teste: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    sucesso = testar_tribos_especificas()
    sys.exit(0 if sucesso else 1)
