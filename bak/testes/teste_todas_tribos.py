"""
Teste de todas as tribos
========================
Este script testa a função analisar_alocacao para todas as tribos disponíveis,
verificando se todas são processadas corretamente.
"""

import os
import pandas as pd
import logging
import traceback
import sys
import json

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('teste_todas_tribos.log')
    ]
)

# Definir caminhos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'dados')
ARQUIVO_ALOCACAO = os.path.join(DATA_DIR, 'Alocacao.xlsx')

def teste_todas_tribos():
    """Testa a função analisar_alocacao para todas as tribos disponíveis"""
    try:
        # Importar a função em um bloco try para capturar erros de importação
        from agenteinsights.analise_insights import analisar_alocacao
        
        # Carregar dados diretamente
        logging.info(f"Carregando dados de {ARQUIVO_ALOCACAO}")
        if not os.path.exists(ARQUIVO_ALOCACAO):
            logging.error(f"Arquivo não encontrado: {ARQUIVO_ALOCACAO}")
            return False
            
        df_alocacao = pd.read_excel(ARQUIVO_ALOCACAO)
        logging.info(f"Dados carregados: {len(df_alocacao)} registros")
        logging.info(f"Colunas disponíveis: {df_alocacao.columns.tolist()}")
        
        # Obter todas as tribos únicas
        tribos = df_alocacao['tribe'].unique().tolist()
        logging.info(f"Total de {len(tribos)} tribos encontradas: {tribos}")
        
        resultados = {}
        falhas = []
        
        # Testar cada tribo
        for tribo in tribos:
            logging.info(f"Testando tribo: {tribo}")
            try:
                resultado = analisar_alocacao(df_alocacao, tribo=tribo)
                # Verificar se temos resultados significativos
                if resultado and resultado['papeis']:
                    logging.info(f"✅ Tribo {tribo}: {len(resultado['papeis'])} papéis encontrados")
                    resultados[tribo] = {
                        'papeis': len(resultado['papeis']),
                        'squads': len(resultado['alocacao_media']),
                        'pessoas_multi_squad': len(resultado['pessoas_multi_squad'])
                    }
                else:
                    logging.warning(f"⚠️ Tribo {tribo}: Sem papéis definidos ou resultado vazio")
                    falhas.append(tribo)
            except Exception as e:
                logging.error(f"❌ Erro ao analisar tribo {tribo}: {str(e)}")
                traceback.print_exc()
                falhas.append(tribo)
        
        # Resumo dos resultados
        logging.info("\n\n======== RESUMO DOS RESULTADOS ========")
        logging.info(f"Total de tribos testadas: {len(tribos)}")
        logging.info(f"Tribos processadas com sucesso: {len(resultados)}")
        logging.info(f"Tribos com falhas: {len(falhas)}")
        
        if falhas:
            logging.info(f"Lista de tribos com falha: {falhas}")
        
        logging.info("\nDetalhes das tribos processadas com sucesso:")
        for tribo, detalhes in sorted(resultados.items()):
            logging.info(f"  - {tribo}: {detalhes['papeis']} papéis, {detalhes['squads']} squads, {detalhes['pessoas_multi_squad']} pessoas em múltiplos squads")
        
        return len(falhas) == 0
        
    except Exception as e:
        logging.error(f"Erro geral no teste: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    sucesso = teste_todas_tribos()
    if sucesso:
        logging.info("✅ Teste concluído com sucesso para todas as tribos!")
        sys.exit(0)
    else:
        logging.error("❌ Teste falhou para algumas tribos")
        sys.exit(1)
