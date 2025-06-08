import pandas as pd
import logging
from pathlib import Path
from analise_ml import executar_analises
from leitura_e_verificacao import carregar_dados, verificar_alteracoes
from cruzamento_dados import cruzar_dados
from gerar_relatorio import gerar_docx
from interacao_ia import iniciar_chat

# Criar diretórios necessários
def criar_diretorios() -> None:
    """Cria os diretórios necessários para o funcionamento do script."""
    diretorios = [
        'output',
        'output/logs',
        'output/modelos',
        'output/graficos',
        'output/relatorios'
    ]
    for diretorio in diretorios:
        Path(diretorio).mkdir(parents=True, exist_ok=True)

# Criar diretórios antes de configurar logging
criar_diretorios()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='output/logs/insights.log',
    encoding='utf-8'
)

def main() -> None:
    """Executa o pipeline principal de análise de dados."""
    try:
        logging.info("Iniciando pipeline de análise...")
        
        # 1. Leitura e verificação
        logging.info("Carregando dados...")
        maturidade, alocacao, executivo = carregar_dados()
        
        if verificar_alteracoes(maturidade, alocacao, executivo):
            # 2. Cruzamento
            logging.info("Cruzando dados...")
            dados_gerais = cruzar_dados(maturidade, alocacao, executivo)

            # 3. Análises
            logging.info("Executando análises...")
            resultados = executar_analises(dados_gerais)

            # 4. Relatório
            logging.info("Gerando relatório...")
            gerar_docx(resultados)

            # 5. Chat com IA
            logging.info("Iniciando chat com IA...")
            iniciar_chat()

            # Exibir resultados principais
            logging.info("Exibindo resultados principais...")
            print("\n=== Análise Descritiva ===")
            print(resultados['descritiva'])

            print("\n=== Coeficientes da Regressão ===")
            for var, coef in resultados['regressao']['coeficientes'].items():
                print(f"{var}: {coef:.4f}")
            print(f"R²: {resultados['regressao']['r2']:.4f}")

            logging.info("Pipeline concluído com sucesso!")
        else:
            logging.info("Nenhuma alteração detectada nos dados. Nada a fazer.")
            print("Nenhuma alteração detectada nos dados.")
            
    except Exception as e:
        logging.error(f"Erro durante a execução: {str(e)}")
        print(f"\nErro durante a execução: {str(e)}")
        print("Verifique o arquivo de log para mais detalhes.")
        raise

if __name__ == "__main__":
    main()
