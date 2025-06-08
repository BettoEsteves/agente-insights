"""
Agente Insights - Módulo Principal
=================================
Versão: 1.2.1
Release: 3
Data: 01/06/2025

Histórico:
- 1.0.0 (Release 0): Versão inicial
- 1.1.0 (Release 1): Adicionado sistema de feedback e logging
- 1.2.0 (Release 2): Correção no processamento de dados e análise ML
- 1.2.1 (Release 3): Corrigido problema no cruzamento de dados

Descrição:
Módulo principal que coordena o fluxo de execução do pipeline de análise.
"""

import pandas as pd
import logging
from datetime import datetime
from pathlib import Path
from colorama import init, Fore, Style
from tqdm import tqdm
import time
from analise_ml import executar_analises
from leitura_e_verificacao import carregar_dados, verificar_alteracoes, salvar_arquivos_anteriores
from cruzamento_dados import cruzar_dados
from gerar_relatorio import gerar_docx
from interacao_ia import iniciar_chat

# Inicializar colorama para cores no Windows
init()

def print_status(mensagem: str, tipo: str = "info") -> None:
    """
    Exibe uma mensagem colorida de status para o usuário.
    
    Args:
        mensagem: A mensagem a ser exibida
        tipo: O tipo de mensagem ('info', 'success', 'error', 'warning')
    """
    prefixos = {
        "info": f"{Fore.BLUE}[INFO]{Style.RESET_ALL}",
        "success": f"{Fore.GREEN}[SUCESSO]{Style.RESET_ALL}",
        "error": f"{Fore.RED}[ERRO]{Style.RESET_ALL}",
        "warning": f"{Fore.YELLOW}[AVISO]{Style.RESET_ALL}"
    }
    print(f"{prefixos.get(tipo, prefixos['info'])} {mensagem}")

def criar_diretorios() -> None:
    """Cria os diretórios necessários para o funcionamento do script."""
    diretorios = [
        'historico',
        'dados',
        'dados/anteriores',
        'dados/atuais',
        'relatorios',
        'logs'
    ]
    
    print_status("Verificando e criando diretórios necessários...", "info")
    
    try:
        for diretorio in tqdm(diretorios, desc="Criando diretórios"):
            Path(diretorio).mkdir(parents=True, exist_ok=True)
            time.sleep(0.1)  # Pequena pausa para visualizar o progresso
        print_status("Diretórios criados com sucesso!", "success")
    except Exception as e:
        print_status(f"Erro ao criar diretórios: {str(e)}", "error")
        logging.error(f"Erro ao criar diretórios: {str(e)}")
        raise

def main() -> None:
    """Função principal que coordena o fluxo de execução do script."""
    data_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Configurar logging
    logging.basicConfig(
        filename=f'logs/execucao_{data_hora}.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    try:
        print_status("Iniciando análise de insights...", "info")
        logging.info("Iniciando execução do script")
        
        # Criar diretórios necessários
        criar_diretorios()        # Carregar e verificar dados
        print_status("Carregando dados...", "info")
        try:
            maturidade, alocacao, executivo = carregar_dados()
            dados_atuais = {
                'maturidade': maturidade,
                'alocacao': alocacao,
                'executivo': executivo
            }
            print_status("Dados carregados com sucesso!", "success")
        except Exception as e:
            print_status(f"Erro ao carregar dados: {str(e)}", "error")
            logging.error(f"Erro ao carregar dados: {str(e)}")
            raise
        
        # Verificar alterações nos dados
        print_status("Verificando alterações nos dados...", "info")
        try:
            alteracoes = verificar_alteracoes(maturidade, alocacao, executivo)
            if alteracoes:
                print_status("Alterações detectadas nos dados.", "warning")
                salvar_arquivos_anteriores(maturidade, alocacao, executivo)
            else:
                print_status("Nenhuma alteração significativa detectada.", "info")
        except Exception as e:
            print_status(f"Erro ao verificar alterações: {str(e)}", "error")
            logging.error(f"Erro ao verificar alterações: {str(e)}")
            raise
          # Executar análises de ML
        print_status("Iniciando análises de machine learning...", "info")
        try:
            # Executar análises para cada conjunto de dados
            resultados_ml = {
                'maturidade': executar_analises(dados_atuais['maturidade']),
                'alocacao': executar_analises(dados_atuais['alocacao']),
                'executivo': executar_analises(dados_atuais['executivo'])
            }
            print_status("Análises de ML concluídas com sucesso!", "success")
        except Exception as e:
            print_status(f"Erro nas análises de ML: {str(e)}", "error")
            logging.error(f"Erro nas análises de ML: {str(e)}")
            raise
        
        # Cruzar dados
        print_status("Cruzando dados...", "info")
        try:
            dados_cruzados = cruzar_dados(
                maturidade=dados_atuais['maturidade'],
                alocacao=dados_atuais['alocacao'],
                executivo=dados_atuais['executivo']
            )
            print_status("Dados cruzados com sucesso!", "success")
            logging.info("Cruzamento de dados concluído")
            
            # Gerar relatório
            print_status("Gerando relatório...", "info")
            try:
                caminho_relatorio = f"relatorios/relatorio_{data_hora}.docx"
                gerar_docx(dados=dados_cruzados, caminho_saida=caminho_relatorio)
                print_status("Relatório gerado com sucesso!", "success")
            except Exception as e:
                print_status(f"Erro ao gerar relatório: {str(e)}", "error")
                logging.error(f"Erro ao gerar relatório: {str(e)}")
                raise

        except Exception as e:
            print_status(f"Erro ao cruzar dados: {str(e)}", "error")
            logging.error(f"Erro ao cruzar dados: {str(e)}")
            raise

        # Iniciar chat para análise
        print_status("Iniciando chat para análise interativa...", "info")
        try:
            iniciar_chat(dados_cruzados)
            print_status("Chat finalizado com sucesso!", "success")
        except Exception as e:
            print_status(f"Erro no chat interativo: {str(e)}", "error")
            logging.error(f"Erro no chat interativo: {str(e)}")
            raise
        
        print_status("Processamento concluído com sucesso!", "success")
        logging.info("Execução do script finalizada com sucesso")
        
    except Exception as e:
        print_status(f"Erro durante a execução: {str(e)}", "error")
        logging.error(f"Erro durante a execução: {str(e)}")
        print_status(f"Erro fatal: {str(e)}", "error")

if __name__ == "__main__":
    init()  # Inicializa colorama
    try:
        main()
    except KeyboardInterrupt:
        print_status("\nOperação cancelada pelo usuário.", "warning")
    except Exception as e:
        print_status(f"Erro fatal: {str(e)}", "error")
