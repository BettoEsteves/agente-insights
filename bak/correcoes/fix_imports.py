"""
Fix Imports - Script para adicionar importações necessárias nos arquivos corrigidos do Agente Insights
======================
Este script adiciona todas as importações que estão faltando nos arquivos corrigidos:
1. chat_ia_loop_corrigido.py
2. gerar_resposta_contextualizada_corrigido.py
3. mapear_estrutura_org_corrigido.py
"""

import os
import re
import shutil
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fix_imports.log'),
        logging.StreamHandler()
    ]
)

def fazer_backup(arquivo):
    """Faz backup do arquivo antes de modificá-lo"""
    backup_dir = os.path.join(os.path.dirname(arquivo), 'backups')
    os.makedirs(backup_dir, exist_ok=True)
    
    # Nome do arquivo de backup com timestamp
    nome_base = os.path.basename(arquivo)
    backup_nome = f"{nome_base}.{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
    backup_path = os.path.join(backup_dir, backup_nome)
    
    # Copiar arquivo original para backup
    shutil.copy2(arquivo, backup_path)
    logging.info(f"Backup criado: {backup_path}")
    
    return backup_path

def adicionar_imports_chat_ia_loop(conteudo):
    """Adiciona as importações necessárias ao arquivo chat_ia_loop_corrigido.py"""
    imports = """import os
import sys
import json
import time
from typing import Dict, Any, List, Optional, Union, Tuple
from dotenv import load_dotenv
from openai import OpenAI
import logging
import traceback

# Importações das funções do sistema
from mapear_estrutura_org_corrigido import mapear_estrutura_org
from gerar_resposta_contextualizada_corrigido import (
    gerar_resposta_contextualizada,
    preparar_dados_consulta,
    identificar_entidade_consulta
)
"""
    
    # Verificar se o arquivo já tem as importações
    if "import os" in conteudo and "from typing import Dict, Any" in conteudo:
        logging.info("Importações já existem em chat_ia_loop_corrigido.py")
        return conteudo
    
    # Adicionar as importações no início do arquivo
    linhas = conteudo.split('\n')
    
    # Encontrar onde começam as definições e comentários
    inicio_real = 0
    for i, linha in enumerate(linhas):
        if linha.startswith("def ") or linha.startswith('#') or 'chat_ia_loop' in linha:
            inicio_real = i
            break
    
    # Adicionar imports antes do início real do código
    novo_conteudo = imports + "\n".join(linhas[inicio_real:])
    
    return novo_conteudo

def adicionar_imports_gerar_resposta(conteudo):
    """Adiciona as importações necessárias ao arquivo gerar_resposta_contextualizada_corrigido.py"""
    imports = """import os
import sys
import json
import re
import string
from typing import Dict, Any, List, Optional, Union, Tuple
from openai import OpenAI
import logging
import traceback
import pandas as pd
from unidecode import unidecode

"""
    
    # Verificar se o arquivo já tem as importações
    if "import os" in conteudo and "from unidecode import unidecode" in conteudo:
        logging.info("Importações já existem em gerar_resposta_contextualizada_corrigido.py")
        return conteudo
    
    # Adicionar as importações no início do arquivo
    linhas = conteudo.split('\n')
    
    # Encontrar onde começam as definições e comentários
    inicio_real = 0
    for i, linha in enumerate(linhas):
        if linha.startswith("def ") or linha.startswith('#') or 'gerar_resposta_contextualizada' in linha:
            inicio_real = i
            break
    
    # Adicionar imports antes do início real do código
    novo_conteudo = imports + "\n".join(linhas[inicio_real:])
    
    return novo_conteudo

def adicionar_imports_mapear_estrutura(conteudo):
    """Adiciona as importações necessárias ao arquivo mapear_estrutura_org_corrigido.py"""
    imports = """import os
import sys
import json
import re
import string
from typing import Dict, Any, List, Optional, Union, Tuple
import pandas as pd
import logging
import traceback
from collections import Counter
from unidecode import unidecode

def normalizar_texto(texto):
    # Normaliza um texto removendo acentos, espaços extras e convertendo para minúsculas
    if not isinstance(texto, str):
        return str(texto).lower()
    
    # Remover acentos
    texto_sem_acentos = unidecode(texto)
    
    # Converter para minúsculo e remover espaços extras
    texto_normalizado = texto_sem_acentos.lower().strip()
    
    # Remover caracteres especiais e substituir espaços por underscore
    texto_normalizado = re.sub(r'[^a-z0-9\s]', '', texto_normalizado)
    texto_normalizado = re.sub(r'\s+', '_', texto_normalizado)
    
    return texto_normalizado
"""
    
    # Verificar se o arquivo já tem as importações
    if "import os" in conteudo and "from unidecode import unidecode" in conteudo:
        logging.info("Importações já existem em mapear_estrutura_org_corrigido.py")
        return conteudo
    
    # Adicionar as importações no início do arquivo
    linhas = conteudo.split('\n')
    
    # Encontrar onde começam as definições e comentários
    inicio_real = 0
    for i, linha in enumerate(linhas):
        if linha.startswith("def ") or linha.startswith('#') or 'mapear_estrutura_org' in linha:
            inicio_real = i
            break
            
    # Se já definir normalizar_texto, não adicionar novamente
    if "def normalizar_texto" in conteudo:
        imports = imports.split("def normalizar_texto")[0]
    
    # Adicionar imports antes do início real do código
    novo_conteudo = imports + "\n".join(linhas[inicio_real:])
    
    return novo_conteudo

def corrigir_importacoes(arquivo, funcao_correcao):
    """Aplica as correções de importações em um arquivo"""
    try:
        # Fazer backup do arquivo
        backup = fazer_backup(arquivo)
        
        # Ler conteúdo do arquivo
        with open(arquivo, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        # Aplicar correções
        conteudo_modificado = funcao_correcao(conteudo)
        
        # Salvar arquivo modificado
        with open(arquivo, 'w', encoding='utf-8') as f:
            f.write(conteudo_modificado)
        
        logging.info(f"Importações adicionadas em {arquivo}")
        return True
        
    except Exception as e:
        logging.error(f"Erro ao corrigir importações em {arquivo}: {str(e)}")
        # Restaurar backup em caso de erro
        try:
            shutil.copy2(backup, arquivo)
            logging.info(f"Arquivo restaurado do backup após erro: {arquivo}")
        except Exception as restore_error:
            logging.error(f"Erro ao restaurar backup: {str(restore_error)}")
        
        return False

def main():
    print("=== Fix Imports - Agente Insights ===")
    print("Este script adicionará as importações necessárias nos arquivos corrigidos.")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    arquivos = [
        os.path.join(base_dir, 'chat_ia_loop_corrigido.py'),
        os.path.join(base_dir, 'gerar_resposta_contextualizada_corrigido.py'),
        os.path.join(base_dir, 'mapear_estrutura_org_corrigido.py')
    ]
    
    # Verificar se os arquivos existem
    arquivos_existentes = []
    for arquivo in arquivos:
        if os.path.exists(arquivo):
            arquivos_existentes.append(arquivo)
        else:
            print(f"❌ Arquivo não encontrado: {arquivo}")
    
    if not arquivos_existentes:
        print("Nenhum arquivo para corrigir foi encontrado.")
        return False
    
    print("\nArquivos a serem modificados:")
    for arquivo in arquivos_existentes:
        print(f"- {arquivo}")
    
    confirmacao = input("\nDeseja prosseguir com as correções? (s/n): ").strip().lower()
    if confirmacao != 's':
        print("Operação cancelada pelo usuário.")
        return False
    
    # Aplicar correções
    resultados = []
    for arquivo in arquivos_existentes:
        nome_arquivo = os.path.basename(arquivo)
        
        if nome_arquivo == 'chat_ia_loop_corrigido.py':
            resultado = corrigir_importacoes(arquivo, adicionar_imports_chat_ia_loop)
        elif nome_arquivo == 'gerar_resposta_contextualizada_corrigido.py':
            resultado = corrigir_importacoes(arquivo, adicionar_imports_gerar_resposta)
        elif nome_arquivo == 'mapear_estrutura_org_corrigido.py':
            resultado = corrigir_importacoes(arquivo, adicionar_imports_mapear_estrutura)
        else:
            logging.warning(f"Arquivo não suportado: {nome_arquivo}")
            continue
        
        resultados.append((nome_arquivo, resultado))
    
    # Mostrar resumo
    print("\n=== Resumo das Correções ===")
    sucessos = sum(1 for _, status in resultados if status)
    falhas = len(resultados) - sucessos
    
    if sucessos == len(resultados):
        print("✅ Todas as importações foram adicionadas com sucesso!")
    elif sucessos > 0:
        print(f"⚠️ {sucessos} de {len(resultados)} arquivos foram corrigidos com sucesso.")
    else:
        print("❌ Nenhum arquivo foi corrigido.")
    
    print("\nDetalhes:")
    for nome, status in resultados:
        status_texto = "✅ Sucesso" if status else "❌ Falha"
        print(f"- {nome}: {status_texto}")
    
    print("\nPróximos passos:")
    print("1. Execute o script para corrigir o arquivo analise_insights.py:")
    print("   python fix_agente_insights.py")
    print("2. Teste o Agente Insights corrigido:")
    print("   python insights.py")
    
    return sucessos > 0

if __name__ == "__main__":
    main()
