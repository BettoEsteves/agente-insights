import pandas as pd
import os
from pathlib import Path

def verificar_arquivos():
    """Verifica a existência e estrutura dos arquivos Excel"""
    # Usar caminho absoluto
    data_dir = Path(__file__).parent / "agenteinsights" / "data"
    
    arquivos = {
        "Maturidade": "MaturidadeT.xlsx",
        "Alocação": "Alocacao.xlsx",
        "Executivo": "Executivo.xlsx"
    }
    
    problemas = []
    
    print(f"\nDiretório de dados: {data_dir}")
    print(f"Diretório existe? {data_dir.exists()}\n")
    
    for nome, arquivo in arquivos.items():
        caminho = data_dir / arquivo
        print(f"\n{'='*50}")
        print(f"Verificando {nome}:")
        print(f"Caminho completo: {caminho.absolute()}")
        
        if caminho.exists():
            try:
                df = pd.read_excel(caminho)
                print("✅ Arquivo encontrado e carregado")
                print(f"\nInformações do DataFrame:")
                print(f"Shape: {df.shape}")
                print("\nPrimeiras 5 linhas:")
                print(df.head())
                print("\nColunas disponíveis:")
                for col in df.columns:
                    print(f"- {col}")
            except Exception as e:
                print(f"❌ Erro ao ler arquivo: {str(e)}")
                problemas.append(f"Erro em {nome}: {str(e)}")
        else:
            print("❌ Arquivo não encontrado")
            problemas.append(f"Arquivo não encontrado: {nome}")
    
    if problemas:
        print("\n⚠️ Problemas encontrados:")
        for p in problemas:
            print(f"- {p}")
    else:
        print("\n✅ Todos os arquivos verificados com sucesso!")

if __name__ == "__main__":
    verificar_arquivos()