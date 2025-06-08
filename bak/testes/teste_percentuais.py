#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste específico para tratamento de percentuais
=============================================
Verifica se a função analisar_alocacao está tratando corretamente
as percentagens em formato de texto com símbolo '%'.
"""

import pandas as pd
import os
import traceback
import sys
import random

try:
    print("\n=== Teste de tratamento de percentuais ===\n")
    
    # Importar funções necessárias
    from agenteinsights.analise_insights import analisar_alocacao
    
    # Carregar dados
    arquivo = os.path.join('dados', 'Alocacao.xlsx')
    
    if os.path.exists(arquivo):
        print(f"Carregando arquivo: {arquivo}")
        df = pd.read_excel(arquivo)
        print(f"Arquivo carregado: {len(df)} registros")
        
        # 1. Verificação de formato atual dos percentuais
        if 'percetageAllocation' in df.columns:
            perc_col = 'percetageAllocation'
        elif 'percentageAllocation' in df.columns:
            perc_col = 'percentageAllocation'
        else:
            perc_col = None
        
        if perc_col:
            print(f"\nColuna de percentual encontrada: {perc_col}")
            
            # Mostrar os tipos e valores únicos
            dtype = df[perc_col].dtype
            print(f"Tipo de dados atual: {dtype}")
            
            # Amostrar alguns valores
            amostra = df[perc_col].sample(min(10, len(df))).tolist()
            print(f"Amostra de valores: {amostra}")
            
            # 2. Testar diferentes formatos
            print("\n== Testando tratamento de diferentes formatos de percentuais ==")
            
            # Criar um DataFrame de teste com diferentes formatos de percentuais
            dados_teste = df.sample(20).copy()
            
            # Modificar os percentuais para diferentes formatos
            formatos = ['50%', '75.5%', '100', 50, 25.5, '33,5%']
            
            for i, idx in enumerate(dados_teste.index):
                dados_teste.loc[idx, perc_col] = formatos[i % len(formatos)]
                
            print(f"Formatos de teste criados: {dados_teste[perc_col].tolist()}")
            
            # 3. Executar a função analisar_alocacao com os dados modificados
            print("\nExecutando analisar_alocacao com dados de teste...")
            resultado = analisar_alocacao(dados_teste)
            
            # 4. Verificar se a função tratou corretamente os percentuais
            print("\nVerificando resultados...")
            print(f"Análise concluída com sucesso!")
            print(f"Papéis encontrados: {len(resultado['papeis'])}")
            print(f"Squads: {len(resultado.get('composicao_squads', {}))}")
            
            # 5. Verificar se os percentuais foram normalizados corretamente
            if 'alocacao_media' in resultado and resultado['alocacao_media']:
                print("\nAlocações médias por squad:")
                for squad, alocacao in resultado['alocacao_media'].items():
                    print(f"  - {squad}: {alocacao:.2f}")
                    # Valores devem estar entre 0 e 1
                    if not (0 <= alocacao <= 1):
                        print(f"    ❌ ERRO: Valor fora do intervalo esperado (0-1)")
    else:
        print(f"❌ Arquivo não encontrado: {arquivo}")
        sys.exit(1)
        
except Exception as e:
    print(f"❌ ERRO: {str(e)}")
    traceback.print_exc()
    sys.exit(1)

print("\n✅ Teste concluído com sucesso!")
