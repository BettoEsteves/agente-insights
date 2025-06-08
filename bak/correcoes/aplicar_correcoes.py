"""
Aplicar Correções Manualmente - Script para substituir as funções do Agente Insights
======================
Este script substitui as três funções corrigidas no arquivo analise_insights.py:
1. chat_ia_loop
2. gerar_resposta_contextualizada
3. mapear_estrutura_org
"""

import os
import shutil
import re
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('aplicar_correcoes.log'),
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

def obter_conteudo_funcao(arquivo):
    """Lê o conteúdo de um arquivo que contém uma função corrigida"""
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            
        # Remover cabeçalho de comentário se existir
        conteudo = re.sub(r'^""".*?"""\s*', '', conteudo, flags=re.DOTALL)
        
        return conteudo.strip()
    except Exception as e:
        logging.error(f"Erro ao ler o arquivo {arquivo}: {str(e)}")
        return None

def substituir_funcao(arquivo_original, padrao_inicio, padrao_fim, novo_conteudo):
    """Substitui uma função no arquivo original"""
    try:
        with open(arquivo_original, 'r', encoding='utf-8') as f:
            conteudo_original = f.read()
        
        # Encontrar início da função
        inicio = conteudo_original.find(padrao_inicio)
        if inicio == -1:
            logging.error(f"Não foi possível encontrar o padrão de início: {padrao_inicio}")
            return False
        
        # Procurar pela próxima função após o início encontrado
        parte_depois = conteudo_original[inicio:]
        match = re.search(padrao_fim, parte_depois)
        if match:
            fim = inicio + match.start()
        else:
            # Se não encontrar a próxima função, assume até o final do arquivo
            fim = len(conteudo_original)
        
        # Construir novo conteúdo
        novo_conteudo_completo = (
            conteudo_original[:inicio] + 
            novo_conteudo + 
            conteudo_original[fim:]
        )
        
        # Salvar arquivo modificado
        with open(arquivo_original, 'w', encoding='utf-8') as f:
            f.write(novo_conteudo_completo)
        
        return True
        
    except Exception as e:
        logging.error(f"Erro ao substituir função: {str(e)}")
        return False

def aplicar_correcoes():
    """Aplica todas as correções necessárias"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    arquivo_original = os.path.join(base_dir, 'agenteinsights', 'analise_insights.py')
    
    # Fazer backup do arquivo original
    backup = fazer_backup(arquivo_original)
    
    # Ler os arquivos com as funções corrigidas
    chat_ia_loop = obter_conteudo_funcao(os.path.join(base_dir, 'chat_ia_loop_corrigido.py'))
    gerar_resposta = obter_conteudo_funcao(os.path.join(base_dir, 'gerar_resposta_contextualizada_corrigido.py'))
    mapear_estrutura = obter_conteudo_funcao(os.path.join(base_dir, 'mapear_estrutura_org_corrigido.py'))
    
    if not chat_ia_loop or not gerar_resposta or not mapear_estrutura:
        logging.error("Falha ao ler arquivos com correções")
        return False
    
    # Padrões para encontrar o início de cada função
    padrao_chat_ia_loop = "def chat_ia_loop(analises: Dict[str, Any]):"
    padrao_mapear_estrutura = "def mapear_estrutura_org(analises: Dict[str, Any]) -> Dict:"
    padrao_gerar_resposta = "def gerar_resposta_contextualizada(query: str, entidade: str, dados: Dict, client: OpenAI) -> str:"
    
    # Padrões para encontrar o fim de cada função (início da próxima função/definição)
    padrao_fim = r"\ndef\s+[a-zA-Z_][a-zA-Z0-9_]*\("
    
    # Aplicar substituições
    substituicoes = [
        (padrao_chat_ia_loop, padrao_fim, chat_ia_loop),
        (padrao_mapear_estrutura, padrao_fim, mapear_estrutura),
        (padrao_gerar_resposta, padrao_fim, gerar_resposta)
    ]
    
    resultados = []
    for (padrao_inicio, padrao_fim, conteudo) in substituicoes:
        sucesso = substituir_funcao(arquivo_original, padrao_inicio, padrao_fim, conteudo)
        resultados.append(sucesso)
    
    # Verificar resultados
    if all(resultados):
        logging.info("Todas as funções foram substituídas com sucesso")
        return True
    else:
        # Restaurar backup em caso de falha
        logging.error("Houve falhas ao substituir as funções")
        try:
            shutil.copy2(backup, arquivo_original)
            logging.info(f"Arquivo restaurado do backup: {backup}")
        except Exception as e:
            logging.error(f"Erro ao restaurar backup: {str(e)}")
        
        return False

def main():
    print("=== Aplicar Correções Manualmente ===")
    print("Este script substitui as funções corrigidas no arquivo analise_insights.py")
    
    confirmacao = 's'  # Automatically confirm
    print("\nProsseguindo com as correções automaticamente...")
    
    sucesso = aplicar_correcoes()
    
    if sucesso:
        print("\n✅ Todas as funções foram substituídas com sucesso!")
        print("\nPróximos passos:")
        print("1. Execute o sistema para testar as correções:")
        print("   python insights.py")
        print("2. Verifique se agora é possível analisar todas as 15 tribos corretamente.")
    else:
        print("\n❌ Houve um problema ao aplicar as correções.")
        print("Verifique o arquivo de log para mais detalhes: aplicar_correcoes.log")

if __name__ == "__main__":
    main()
