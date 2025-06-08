"""
Script de teste para o Agente Insights
====================================
"""

import os
import logging
from analise_insights import testar_mapeamento, DATA_DIR, ARQUIVO_MATURIDADE, ARQUIVO_ALOCACAO, ARQUIVO_EXECUTIVO

def verificar_ambiente():
    """Verifica se o ambiente está configurado corretamente"""
    print("\nVerificando ambiente...")
    
    # Verificar diretório de dados
    if not os.path.exists(DATA_DIR):
        print(f"❌ Diretório de dados não encontrado: {DATA_DIR}")
        print("Criando diretório...")
        os.makedirs(DATA_DIR)
    else:
        print(f"✅ Diretório de dados encontrado: {DATA_DIR}")
    
    # Verificar arquivos necessários
    arquivos = {
        'Maturidade': ARQUIVO_MATURIDADE,
        'Alocação': ARQUIVO_ALOCACAO,
        'Executivo': ARQUIVO_EXECUTIVO
    }
    
    arquivos_faltando = []
    for nome, caminho in arquivos.items():
        if not os.path.exists(caminho):
            print(f"❌ Arquivo {nome} não encontrado: {caminho}")
            arquivos_faltando.append(nome)
        else:
            print(f"✅ Arquivo {nome} encontrado: {caminho}")
    
    if arquivos_faltando:
        print("\n⚠️ Arquivos necessários faltando:")
        for arquivo in arquivos_faltando:
            print(f"- {arquivo}")
        print("\nPor favor, coloque os arquivos no diretório:")
        print(DATA_DIR)
        return False
    
    return True

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Iniciando testes...")
    
    # Verificar ambiente primeiro
    if not verificar_ambiente():
        logging.error("Ambiente não configurado corretamente")
        return
    
    # Executar teste de mapeamento
    sucesso = testar_mapeamento()
    
    if sucesso:
        logging.info("Testes concluídos com sucesso!")
    else:
        logging.error("Falha nos testes!")

if __name__ == "__main__":
    main()