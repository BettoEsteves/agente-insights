import os
import shutil
from pathlib import Path

def configurar_ambiente():
    """Configura o ambiente inicial do projeto"""
    try:
        # Definir diretórios
        projeto_dir = Path(__file__).parent
        pacote_dir = projeto_dir / 'agenteinsights'
        data_dir = projeto_dir / 'dados'
        output_dir = projeto_dir / 'output'
        
        # Criar estrutura de diretórios
        diretorios = [
            data_dir,
            output_dir,
            output_dir / 'graficos',
            output_dir / 'relatorios'
        ]
        
        for dir in diretorios:
            dir.mkdir(parents=True, exist_ok=True)
            print(f"✅ Diretório criado: {dir}")
          # Verificar arquivos Excel e configuração
        arquivos_req = {
            'MaturidadeT.xlsx': data_dir / 'MaturidadeT.xlsx',
            'Alocacao.xlsx': data_dir / 'Alocacao.xlsx',
            'Executivo.xlsx': data_dir / 'Executivo.xlsx',
            'config.py': pacote_dir / 'config.py'
        }
        
        for nome, caminho in arquivos_req.items():
            if not caminho.exists():
                print(f"❌ Arquivo não encontrado: {nome}")
                return False  # Retorna False imediatamente se faltar algum arquivo
            else:
                print(f"✅ Arquivo encontrado: {nome}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro na configuração: {str(e)}")
        return False

if __name__ == "__main__":
    configurar_ambiente()