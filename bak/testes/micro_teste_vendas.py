"""
Micro-teste para Vendas
=====================
Testa apenas a função analisar_alocacao para Vendas
"""

import pandas as pd
import os
import traceback

try:
    print("Iniciando teste simplificado para a tribo Vendas")
    
    # Importar apenas a função necessária
    from agenteinsights.analise_insights import analisar_alocacao
    
    # Carregar dados
    arquivo = os.path.join('dados', 'Alocacao.xlsx')
    if os.path.exists(arquivo):
        df = pd.read_excel(arquivo)
        print(f"Arquivo carregado: {len(df)} registros")
        
        # Testar a função
        resultado = analisar_alocacao(df, tribo="Vendas")
        
        # Mostrar resultado
        print(f"Análise realizada com sucesso para tribo Vendas")
        print(f"Papéis encontrados: {list(resultado['papeis'].keys())}")
        print(f"Squads: {list(resultado['composicao_squads']['role'].keys()) if resultado['composicao_squads'] and 'role' in resultado['composicao_squads'] else 'Nenhum'}")
        
        # Testar também Benefícios para comparação
        print("\nTeste comparativo para tribo Benefícios:")
        resultado2 = analisar_alocacao(df, tribo="Benefícios")
        print(f"Análise realizada com sucesso para tribo Benefícios")
        print(f"Papéis encontrados: {list(resultado2['papeis'].keys())}")
        print(f"Squads: {list(resultado2['composicao_squads']['role'].keys()) if resultado2['composicao_squads'] and 'role' in resultado2['composicao_squads'] else 'Nenhum'}")
        
    else:
        print(f"Arquivo não encontrado: {arquivo}")
        
except Exception as e:
    print(f"ERRO: {str(e)}")
    traceback.print_exc()
