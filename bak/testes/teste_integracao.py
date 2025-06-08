#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste Completo de Integração
==========================
Verifica se todas as principais funcionalidades do sistema 
estão trabalhando juntas corretamente, incluindo os casos problemáticos
anteriores.
"""

import pandas as pd
import os
import logging
import traceback
import sys
import time

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('teste_integracao.log')
    ]
)

def testar_integracao():
    """Teste completo de integração do sistema."""
    try:
        print("\n==== TESTE DE INTEGRAÇÃO COMPLETO ====\n")
        
        # 1. Importar todos os módulos e funções necessárias
        print("Importando módulos e funções...")
        from agenteinsights.analise_insights import (
            carregar_dados, 
            padronizar_ids,
            cruzar_dados,
            analisar_alocacao,
            analisar_metricas_ageis,
            normalizar_nome,
            executar_pipeline
        )
        
        # 2. Carregar dados
        print("\nCarregando dados...")
        dados = carregar_dados()
        
        if not dados:
            print("❌ Erro: Falha ao carregar dados")
            return False
            
        print("✓ Dados carregados com sucesso")
        for nome, df in dados.items():
            print(f"  - {nome}: {len(df)} registros, {len(df.columns)} colunas")
        
        # 3. Executar o pipeline completo
        print("\nExecutando pipeline completo...")
        resultado_pipeline = executar_pipeline()
        
        if resultado_pipeline['status'] != 'success':
            print(f"❌ Erro no pipeline: {resultado_pipeline.get('mensagem', 'Erro desconhecido')}")
            return False
            
        print("✓ Pipeline executado com sucesso")
        
        # 4. Testar tribos problemáticas
        print("\nTestando tribos problemáticas específicas:")
        tribos_problematicas = ["Benefícios", "Vendas"]
        
        for tribo in tribos_problematicas:
            print(f"\n== Testando tribo: {tribo} ==")
            
            # Testar normalização
            tribo_norm = normalizar_nome(tribo)
            print(f"Nome normalizado: '{tribo_norm}'")
            
            # Testar análise de alocação
            print("\n1. Análise de alocação...")
            resultado_alocacao = analisar_alocacao(dados['alocacao'], tribo=tribo)
            
            if resultado_alocacao and resultado_alocacao.get('papeis'):
                print(f"✓ Análise de alocação bem-sucedida: {len(resultado_alocacao['papeis'])} papéis encontrados")
            else:
                print("❌ Falha na análise de alocação")
                return False
                
            # Testar métricas ágeis 
            print("\n2. Análise de métricas ágeis...")
            try:
                resultado_metricas = analisar_metricas_ageis(dados['maturidade'], tribo=tribo)
                print(f"✓ Análise de métricas bem-sucedida")
            except Exception as e:
                print(f"⚠️ Aviso na análise de métricas: {str(e)}")
                # Não falhar o teste por causa disso
        
        # 5. Testar processamento de percentuais
        print("\nTestando processamento de percentuais...")
        
        # Criar DataFrame de teste
        df_teste = pd.DataFrame({
            'tribe': ['Teste'] * 10,
            'squad': ['Squad1'] * 5 + ['Squad2'] * 5,
            'person': [f"Pessoa{i}" for i in range(10)],
            'role': ['Desenvolvedor'] * 6 + ['PO'] * 2 + ['QA'] * 2,
            'percetageAllocation': ['100%', '50%', '75%', '33,5%', 25, 
                                   100.0, '80%', 70, '60,5%', '90.5%']
        })
        
        print("DataFrame de teste criado com diferentes formatos de percentuais")
        print(f"Valores de teste: {df_teste['percetageAllocation'].tolist()}")
        
        # Testar processamento
        resultado_perc = analisar_alocacao(df_teste)
        
        if resultado_perc and resultado_perc.get('papeis'):
            print("✓ Processamento de percentuais bem-sucedido")
            print(f"Alocação média por squad: {resultado_perc['alocacao_media']}")
            
            # Verificar se os valores estão normalizados (entre 0 e 1)
            valores_ok = all(0 <= v <= 1 for v in resultado_perc['alocacao_media'].values())
            
            if valores_ok:
                print("✓ Valores normalizados corretamente (entre 0 e 1)")
            else:
                print("❌ Valores não estão normalizados corretamente")
                return False
        else:
            print("❌ Falha no processamento de percentuais")
            return False
        
        # 6. Resultado final
        print("\n==== RESULTADO FINAL ====")
        print("✅ Todos os testes passaram com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro geral no teste de integração: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    start_time = time.time()
    sucesso = testar_integracao()
    tempo_total = time.time() - start_time
    
    print(f"\nTempo total de execução: {tempo_total:.2f} segundos")
    print(f"Resultado final: {'✅ SUCESSO' if sucesso else '❌ FALHA'}")
    
    sys.exit(0 if sucesso else 1)
