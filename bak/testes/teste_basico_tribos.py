"""
Teste das tribos com caminho absoluto
"""
import pandas as pd
import os

try:
    print("Teste básico de tribos")
    
    # Importar função
    from agenteinsights.analise_insights import analisar_alocacao
    print("Importação concluída com sucesso")
    
    # Caminho absoluto
    caminho = r'e:\Projeto\Agente_Insights\dados\Alocacao.xlsx'
    print(f"Arquivo existe? {os.path.exists(caminho)}")
    
    # Carregar dados
    df = pd.read_excel(caminho)
    print(f"Arquivo carregado: {len(df)} linhas, {df.columns.tolist()}")
    
    # Listar tribos
    tribos = df['tribe'].unique()
    print(f"Tribos encontradas: {tribos}")
    
    # Testar cada tribo
    for tribo in ['Benefícios', 'Vendas']:
        print(f"\nTestando tribo: {tribo}")
        if tribo in tribos:
            try:
                resultado = analisar_alocacao(df, tribo=tribo)
                print(f"✓ Sucesso: {len(resultado['papeis'])} papéis")
            except Exception as e:
                print(f"✗ Erro: {str(e)}")
        else:
            print(f"✗ Tribo não encontrada")
            
except Exception as e:
    print(f"Erro geral: {str(e)}")
