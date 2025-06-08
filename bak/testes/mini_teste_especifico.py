#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Mini teste para Benefícios e Vendas
=================================
Testa apenas a função analisar_alocacao para as tribos problemáticas.
"""

import pandas as pd
import os
import traceback
import sys

try:
    print("\n=== Mini teste para tribos problemáticas ===\n")
    
    # Importar apenas a função necessária
    from agenteinsights.analise_insights import analisar_alocacao, normalizar_nome
    
    # Carregar dados
    arquivo = os.path.join('dados', 'Alocacao.xlsx')
    
    if os.path.exists(arquivo):
        print(f"Carregando arquivo: {arquivo}")
        df = pd.read_excel(arquivo)
        print(f"Arquivo carregado: {len(df)} registros")
        
        # Verificar colunas disponíveis
        print(f"Colunas disponíveis: {df.columns.tolist()}")
        
        # Adicionar coluna tribe_norm para normalização
        if 'tribe_norm' not in df.columns:
            print("Criando coluna tribe_norm...")
            df['tribe_norm'] = df['tribe'].apply(normalizar_nome)
        
        # Testar cada tribo problemática
        tribos = ["Benefícios", "Vendas"]
        
        for tribo in tribos:
            print(f"\n== Testando tribo: {tribo} ==")
            
            # Verificar contagem de registros
            tribo_norm = normalizar_nome(tribo)
            print(f"Nome normalizado: '{tribo_norm}'")
            
            count_original = len(df[df['tribe'] == tribo])
            count_norm = len(df[df['tribe_norm'] == tribo_norm])
            
            print(f"Registros (busca original): {count_original}")
            print(f"Registros (busca normalizada): {count_norm}")
            
            # Testar função analisar_alocacao
            print(f"\nExecutando analisar_alocacao para {tribo}...")
            resultado = analisar_alocacao(df, tribo=tribo)
            
            # Imprimir resultados
            print(f"Análise concluída!")
            print(f"Papéis encontrados: {list(resultado['papeis'].keys())}")
            print(f"Total de papéis: {len(resultado['papeis'])}")
            print(f"Squads: {list(resultado.get('composicao_squads', {}).keys())}")
            print(f"Total de squads: {len(resultado.get('composicao_squads', {}))}")
            
            # Verificar composição de squads se disponível
            if 'composicao_squads' in resultado and resultado['composicao_squads']:
                for squad, info in resultado['composicao_squads'].items():
                    papeis_squad = info.get('role', {})
                    if papeis_squad:
                        print(f"\nPapéis no squad {squad}:")
                        for papel, qtd in papeis_squad.items():
                            print(f"  - {papel}: {qtd}")
    else:
        print(f"❌ Arquivo não encontrado: {arquivo}")
        sys.exit(1)
        
except Exception as e:
    print(f"❌ ERRO: {str(e)}")
    traceback.print_exc()
    sys.exit(1)

print("\n✅ Teste concluído com sucesso!")
