"""
Teste de Maturidade de Todas as Tribos
====================================
Este script testa se todas as tribos estão sendo carregadas corretamente com suas maturidades.
"""

import pandas as pd
import os
import logging
from pathlib import Path
import sys
import traceback
from pprint import pformat

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('teste_maturidade_tribos.log'),
        logging.StreamHandler()
    ]
)

def testar_maturidade_tribos():
    """Testa o carregamento e processamento da maturidade de todas as tribos"""
    try:
        # Importar funções necessárias
        from agenteinsights.analise_insights import carregar_dados, mapear_estrutura_org
        
        # Carregar dados
        logging.info("Carregando dados...")
        dados = carregar_dados()
        
        if not dados or not isinstance(dados, dict):
            logging.error("Falha ao carregar dados")
            return False
            
        # Verificar dados carregados
        for nome, df in dados.items():
            if df is None or df.empty:
                logging.warning(f"DataFrame {nome} está vazio")
            else:
                logging.info(f"DataFrame {nome} carregado com {len(df)} registros e {len(df.columns)} colunas")
        
        # Verificar dados de maturidade
        if 'maturidade' not in dados or dados['maturidade'] is None or dados['maturidade'].empty:
            logging.error("Dados de maturidade não encontrados ou vazios")
            return False
            
        df_maturidade = dados['maturidade']
        logging.info(f"Colunas em maturidade: {df_maturidade.columns.tolist()}")
        
        if 'Tribo' not in df_maturidade.columns:
            logging.error("Coluna 'Tribo' não encontrada em dados de maturidade")
            return False
            
        if 'Maturidade' not in df_maturidade.columns:
            logging.error("Coluna 'Maturidade' não encontrada em dados de maturidade")
            return False
        
        # Listar todas as tribos no arquivo de maturidade
        tribos_maturidade = df_maturidade['Tribo'].unique()
        logging.info(f"Tribos em arquivo de maturidade ({len(tribos_maturidade)}): {tribos_maturidade}")
        
        # Mapear estrutura organizacional
        logging.info("Mapeando estrutura organizacional...")
        estrutura = mapear_estrutura_org(dados)
        
        if not estrutura or not isinstance(estrutura, dict):
            logging.error("Falha ao mapear estrutura organizacional")
            return False
            
        # Verificar tribos mapeadas
        tribos_mapeadas = list(estrutura['tribos'].keys())
        logging.info(f"Tribos mapeadas na estrutura ({len(tribos_mapeadas)}): {tribos_mapeadas}")
        
        # Verificar maturidades mapeadas
        maturidades = estrutura.get('maturidades', {})
        logging.info(f"Maturidades mapeadas ({len(maturidades)}): {pformat(maturidades)}")
        
        # Verificar se todas as tribos do arquivo de maturidade foram mapeadas
        tribos_nao_encontradas = []
        for tribo in tribos_maturidade:
            if tribo not in tribos_mapeadas and tribo not in maturidades:
                tribos_nao_encontradas.append(tribo)
                
        if tribos_nao_encontradas:
            logging.warning(f"Tribos nos dados de maturidade que não foram mapeadas: {tribos_nao_encontradas}")
        
        # Verificar se cada tribo na estrutura tem um valor de maturidade
        tribos_sem_maturidade = []
        for tribo in tribos_mapeadas:
            if 'maturidade' not in estrutura['tribos'][tribo] and tribo not in maturidades:
                tribos_sem_maturidade.append(tribo)
                
        if tribos_sem_maturidade:
            logging.warning(f"Tribos sem valor de maturidade: {tribos_sem_maturidade}")
        
        # Teste considerado bem-sucedido se todas as tribos de maturidade foram mapeadas
        sucesso = len(tribos_nao_encontradas) == 0
        
        if sucesso:
            logging.info("✅ Todas as tribos do arquivo de maturidade foram mapeadas corretamente")
        else:
            logging.warning(f"❌ {len(tribos_nao_encontradas)} tribos não foram mapeadas corretamente")
            
        return sucesso
        
    except Exception as e:
        logging.error(f"Erro ao testar maturidade das tribos: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== Teste de Maturidade de Todas as Tribos ===")
    
    resultado = testar_maturidade_tribos()
    
    if resultado:
        print("\n✅ Teste concluído com sucesso!")
        print("Todas as tribos foram corretamente mapeadas com suas maturidades.")
        sys.exit(0)
    else:
        print("\n❌ Teste falhou")
        print("Verifique o arquivo de log para mais detalhes: teste_maturidade_tribos.log")
        sys.exit(1)
