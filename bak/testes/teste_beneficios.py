"""
Teste da tribo Benefícios
========================
Este script testa especificamente o processamento da tribo Benefícios,
que estava apresentando problemas anteriormente.
"""

import os
import pandas as pd
import sys
import json
import traceback

try:
    # Importar a função para análise
    from agenteinsights.analise_insights import analisar_alocacao, carregar_dados
    
    # Método 1: Usar a função carregar_dados para obter todos os dados
    print("Método 1: Utilizando carregar_dados()")
    try:
        dados = carregar_dados()
        if 'alocacao' in dados:
            print(f"  ✓ Dados carregados com sucesso. Quantidade: {len(dados['alocacao'])} registros")
            resultado = analisar_alocacao(dados['alocacao'], 'Benefícios')
            print(f"  ✓ Resultado para Benefícios: {json.dumps(resultado, indent=2)}")
        else:
            print(f"  ✗ Falha: Chave 'alocacao' não encontrada em dados. Chaves disponíveis: {list(dados.keys())}")
    except Exception as e:
        print(f"  ✗ Erro ao usar carregar_dados(): {str(e)}")
        traceback.print_exc()
    
    # Método 2: Carregar o arquivo diretamente
    print("\nMétodo 2: Carregando arquivo diretamente")
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        arquivo = os.path.join(base_dir, 'dados', 'Alocacao.xlsx')
        print(f"  Carregando arquivo: {arquivo}")
        
        if os.path.exists(arquivo):
            df = pd.read_excel(arquivo)
            print(f"  ✓ Arquivo carregado com sucesso. Quantidade: {len(df)} registros")
            tribos = df['tribe'].unique().tolist()
            print(f"  ✓ Tribos disponíveis: {tribos}")
            
            if 'Benefícios' in tribos:
                resultado = analisar_alocacao(df, 'Benefícios')
                print(f"  ✓ Análise para Benefícios concluída com sucesso")
                # Mostrar apenas alguns dados para não poluir a saída
                print(f"  - Papéis encontrados: {list(resultado['papeis'].keys())}")
                print(f"  - Squads encontrados: {list(resultado['alocacao_media'].keys())}")
                print(f"  - Pessoas em múltiplos squads: {len(resultado['pessoas_multi_squad'])}")
            else:
                print(f"  ✗ Tribo Benefícios não encontrada nas tribos disponíveis")
        else:
            print(f"  ✗ Arquivo não encontrado: {arquivo}")
    except Exception as e:
        print(f"  ✗ Erro ao carregar arquivo diretamente: {str(e)}")
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
