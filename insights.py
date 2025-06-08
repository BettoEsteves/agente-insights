"""
Agente Insights - Módulo Principal
=================================
Versão: 1.5.3
Release: 7
Data: 05/06/2025

Histórico:
- 1.0.0 (Release 0): Versão inicial
- 1.1.0 (Release 1): Adicionado sistema de feedback e logging
- 1.2.0 (Release 2): Correção no processamento de dados e análise ML
- 1.2.1 (Release 3): Corrigido problema no cruzamento de dados
- 1.5.0 (Release 4): Implementado novo sistema de análise de maturidade
- 1.5.1 (Release 5): Corrigido merge de tribos usando nomes ao invés de IDs
- 1.5.2 (Release 6): Melhorias na identificação de entidades e tratamento de NoneType
- 1.5.3 (Release 7): Implementação de análises consultivas avançadas e validações robustas

Descrição:
Módulo principal que coordena o fluxo de execução do pipeline de análise.
Implementa análises consultivas de alto nível para gestão organizacional.
"""

import logging
import sys
import traceback
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

from agenteinsights.analise_insights import (
    executar_pipeline,
    chat_ia_loop,
    analisar_alocacao,
    mapear_estrutura_org,
    carregar_dados,
    gerar_analise_consultiva,
    formatar_analise_consultiva,
    gerar_resposta_contextualizada,
    identificar_entidade_consulta,
    preparar_dados_consulta,
    extrair_metricas_ageis
)
from setup_env import configurar_ambiente

def configurar_logging():
    """Configura o sistema de logging com níveis detalhados"""
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = log_dir / f'agente_insights_{timestamp}.log'
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    # Configura logging específico para análises
    analise_logger = logging.getLogger('analise')
    analise_logger.setLevel(logging.INFO)
    analise_handler = logging.FileHandler(log_dir / f'analise_{timestamp}.log')
    analise_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    analise_logger.addHandler(analise_handler)

def validar_ambiente() -> bool:
    """Validação completa do ambiente de execução"""
    try:
        if not configurar_ambiente():
            logging.error("Falha na configuração básica do ambiente")
            return False
            
        # Validações adicionais
        required_dirs = ['dados', 'output', 'logs']
        for dir_name in required_dirs:
            dir_path = Path(dir_name)
            if not dir_path.exists():
                dir_path.mkdir(exist_ok=True)
                logging.info(f"Diretório {dir_name} criado")
                
        return True
    except Exception as e:
        logging.error(f"Erro na validação do ambiente: {str(e)}")
        return False

def main() -> int:
    """Função principal com tratamento robusto de erros"""
    try:
        # Configurar logging
        configurar_logging()
        logging.info("Iniciando Agente Insights v1.5.3")
        
        # Validar ambiente
        logging.info("Validando ambiente de execução...")
        if not validar_ambiente():
            logging.error("Falha na validação do ambiente")
            return 1
        
        # Executar pipeline
        logging.info("Iniciando execução do pipeline principal...")
        analises = executar_pipeline()
        
        if not analises:
            logging.error("Pipeline não gerou análises válidas")
            return 1
            
        # Resumo das análises
        logging.info("Pipeline executado com sucesso!")
        print("\n=== Agente Insights v1.5.3 ===")
        print(f"Análises geradas: {len(analises)}")
        print("Tipos de análise:")
        for analise in analises:
            if isinstance(analise, dict):
                print(f"- {analise.get('tipo', 'N/A')}: {analise.get('descricao', 'N/A')}")
        print("\nIniciando modo interativo.")
        print("Digite 'sair' para encerrar o programa.")
        print("===========================\n")
        
        # Iniciar loop de chat
        return chat_ia_loop(analises)
            
    except Exception as e:
        logging.exception("Erro fatal durante a execução")
        print(f"\n[ERROR] Erro fatal: {str(e)}")
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())