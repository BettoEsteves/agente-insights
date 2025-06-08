"""
Script de inicialização do ambiente
==================================
Este script verifica se o ambiente está configurado corretamente e cria um ambiente
virtual Python caso necessário.
"""

import os
import sys
import subprocess
from pathlib import Path

# Diretório do projeto
PROJETO_DIR = Path(__file__).parent.absolute()
ENV_DIR = PROJETO_DIR / "env"
PYTHON = str(ENV_DIR / "Scripts" / "python.exe")

def verificar_ambiente():
    """Verifica se o ambiente virtual Python está configurado"""
    if not ENV_DIR.exists() or not (ENV_DIR / "Scripts" / "python.exe").exists():
        print("Ambiente virtual não encontrado. Criando...")
        subprocess.run([sys.executable, "-m", "venv", str(ENV_DIR)], check=True)
        print(f"Ambiente virtual criado em {ENV_DIR}")
    
    # Instalar dependências
    print("Instalando dependências...")
    subprocess.run([
        str(ENV_DIR / "Scripts" / "pip.exe"), 
        "install", 
        "-r", 
        str(PROJETO_DIR / "requirements.txt")
    ], check=True)
    
    # Instalar o pacote em modo de desenvolvimento
    print("Instalando pacote local...")
    subprocess.run([
        str(ENV_DIR / "Scripts" / "pip.exe"), 
        "install",
        "-e", 
        "."
    ], check=True)
    
    print("Ambiente configurado com sucesso!")

def inicializar_diretorios():
    """Inicializa os diretórios do projeto"""
    # Diretórios necessários
    diretorios = [
        PROJETO_DIR / "dados",
        PROJETO_DIR / "output",
        PROJETO_DIR / "output" / "graficos",
        PROJETO_DIR / "output" / "relatorios",
        PROJETO_DIR / "bak"
    ]
    
    # Criar diretórios
    for diretorio in diretorios:
        diretorio.mkdir(parents=True, exist_ok=True)
        print(f"Diretório criado/verificado: {diretorio}")
    
    # Verificar arquivos Excel
    arquivos_xlsx = [
        "Alocacao.xlsx",
        "Executivo.xlsx",
        "MaturidadeT.xlsx"
    ]
    
    for arquivo in arquivos_xlsx:
        # Verificar se o arquivo existe na pasta dados
        dados_arquivo = PROJETO_DIR / "dados" / arquivo
        if dados_arquivo.exists():
            print(f"Arquivo encontrado: {dados_arquivo}")
        else:
            print(f"Arquivo não encontrado: {dados_arquivo}")
            
            # Verificar se o arquivo existe na pasta agenteinsights/data
            data_arquivo = PROJETO_DIR / "agenteinsights" / "data" / arquivo
            if data_arquivo.exists():
                # Copiar para a pasta dados
                import shutil
                shutil.copy(data_arquivo, dados_arquivo)
                print(f"Arquivo copiado de {data_arquivo} para {dados_arquivo}")
            else:
                print(f"AVISO: Arquivo {arquivo} não encontrado!")

if __name__ == "__main__":
    print("=== Configuração do Ambiente Agente Insights ===")
    verificar_ambiente()
    inicializar_diretorios()
    print("\nAmbiente pronto! Você pode executar o aplicativo com:")
    print(f"cd {PROJETO_DIR} && {PYTHON} insights.py")
    print("================================================")
