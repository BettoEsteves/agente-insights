"""
Agente Insights - Módulo Principal
=================================
Versão: 1.5.0
Release: 5
Data: 02/06/2025

Descrição:
Módulo principal que coordena o fluxo de execução do pipeline de análise e chat IA.
"""

import logging
from datetime import datetime
from pathlib import Path
from colorama import init, Fore, Style
from tqdm import tqdm
import time

from analise_insights import (
    carregar_dados,
    cruzar_dados,
    executar_analises,
    gerar_graficos,
    executar_pipeline,
    chat_ia_loop
)

def print_status(msg, tipo="info"):
    cores = {
        "info": Fore.CYAN,
        "success": Fore.GREEN,
        "warning": Fore.YELLOW,
        "error": Fore.RED
    }
    print(cores.get(tipo, Fore.WHITE) + f"[{tipo.upper()}] {msg}" + Style.RESET_ALL)

def criar_diretorios():
    diretorios = ["output", "output/graficos", "output/logs", "output/relatorios"]
    print_status("Verificando e criando diretórios necessários...", "info")
    for d in tqdm(diretorios, desc="Criando diretórios"):
        Path(d).mkdir(parents=True, exist_ok=True)
        time.sleep(0.05)
    print_status("Diretórios criados com sucesso!", "success")

def main():
    data_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
    logging.basicConfig(
        filename=f'output/logs/execucao_{data_hora}.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    init(autoreset=True)
    logging.info("Iniciando execução do script")

    try:
        print_status("Iniciando análise de insights...", "info")
        criar_diretorios()

        print_status("Carregando dados...", "info")
        dados = carregar_dados()
        print_status("Dados carregados com sucesso!", "success")

        print_status("Cruzando dados...", "info")
        dados_cruzados = cruzar_dados(dados)
        print_status("Dados cruzados com sucesso!", "success")

        print_status("Executando análises de ML...", "info")
        resultados = executar_analises(dados_cruzados)
        print_status("Análises de ML concluídas com sucesso!", "success")

        print_status("Gerando gráficos...", "info")
        gerar_graficos(dados_cruzados, resultados)
        print_status("Gráficos gerados com sucesso!", "success")

        print_status("Abrindo chat IA para consultas...", "info")
        try:
            analises = {
                "dados": dados,
                "dados_cruzados": dados_cruzados,
                "descritiva": resultados.get("estatisticas"),
                "preditiva": resultados.get("regressao"),
                "diagnostica": resultados.get("clustering")
            }
            chat_ia_loop(analises)
        except Exception as e:
            print_status(f"Erro ao executar chat IA: {str(e)}", "error")
            logging.error(f"Erro ao executar chat IA: {str(e)}")
            raise

    except Exception as e:
        print_status(f"Erro durante a execução: {str(e)}", "error")
        logging.error(f"Erro durante a execução: {str(e)}")
        print_status("Erro fatal: " + str(e), "error")

if __name__ == "__main__":
    main()
