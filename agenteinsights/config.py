from pathlib import Path

# Diretórios
BASE_DIR = Path(__file__).parent.parent  # Sobe um nível
DATA_DIR = BASE_DIR / "dados"  # Usa 'dados' em vez de 'data'
OUTPUT_DIR = BASE_DIR / "output"
GRAFICOS_DIR = OUTPUT_DIR / "graficos"
RELATORIOS_DIR = OUTPUT_DIR / "relatorios"

# Arquivos
ARQUIVO_MATURIDADE = DATA_DIR / "MaturidadeT.xlsx"
ARQUIVO_ALOCACAO = DATA_DIR / "Alocacao.xlsx"
ARQUIVO_EXECUTIVO = DATA_DIR / "Executivo.xlsx"

# Colunas para merge (baseado nos dados reais)
COLUNA_MERGE_MATURIDADE = "ID_Tribo_Alocacao"  # Coluna da tabela de maturidade
COLUNA_MERGE_ALOCACAO = "tribeID"              # Coluna da tabela de alocação