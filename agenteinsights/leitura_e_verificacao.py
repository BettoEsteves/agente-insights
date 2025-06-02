"""
Agente Insights - Módulo de Leitura e Verificação
===============================================
Versão: 1.1.0
Release: 2
Data: 01/06/2025

Histórico:
- 1.0.0 (Release 0): Versão inicial
- 1.1.0 (Release 2): Correção no retorno das funções e validação de dados

Descrição:
Módulo responsável pela leitura dos arquivos de dados e verificação
de alterações entre as versões anteriores e atuais dos dados.
"""

import pandas as pd
import os

def carregar_dados():
    # Carregar os arquivos Excel
    maturidade = pd.read_excel('MaturidadeT.xlsx', 
                             sheet_name='FT_Pesquisa_Nota_Maturidade_Por', 
                             engine='openpyxl')
    alocacao = pd.read_excel('Alocacao.xlsx', 
                            sheet_name='Allocation', 
                            engine='openpyxl')
    executivo = pd.read_excel('Executivo.xlsx', 
                             sheet_name='NewBusinessAgility', 
                             engine='openpyxl')
    
    return maturidade, alocacao, executivo

def verificar_alteracoes(maturidade, alocacao, executivo):
    # Verificar se os arquivos anteriores existem
    arquivos_anteriores = [
        'output/maturidade_anterior.xlsx',
        'output/alocacao_anterior.xlsx',
        'output/executivo_anterior.xlsx'
    ]
    
    # Criar diretório output se não existir
    os.makedirs('output', exist_ok=True)
    
    if not all(os.path.exists(arquivo) for arquivo in arquivos_anteriores):
        return True
    
    # Carregar os arquivos anteriores
    maturidade_anterior = pd.read_excel(arquivos_anteriores[0], engine='openpyxl')
    alocacao_anterior = pd.read_excel(arquivos_anteriores[1], engine='openpyxl')
    executivo_anterior = pd.read_excel(arquivos_anteriores[2], engine='openpyxl')
    
    # Comparar os arquivos
    alteracao_maturidade = not maturidade.equals(maturidade_anterior)
    alteracao_alocacao = not alocacao.equals(alocacao_anterior)
    alteracao_executivo = not executivo.equals(executivo_anterior)
    
    return alteracao_maturidade or alteracao_alocacao or alteracao_executivo

def salvar_arquivos_anteriores(maturidade, alocacao, executivo):
    # Criar diretório output se não existir
    os.makedirs('output', exist_ok=True)
    
    # Salvar os arquivos atuais como versões anteriores
    maturidade.to_excel('output/maturidade_anterior.xlsx', 
                       index=False, 
                       engine='openpyxl')
    alocacao.to_excel('output/alocacao_anterior.xlsx', 
                      index=False, 
                      engine='openpyxl')
    executivo.to_excel('output/executivo_anterior.xlsx', 
                      index=False, 
                      engine='openpyxl')
