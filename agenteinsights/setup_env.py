import os
import shutil
from pathlib import Path

def configurar_ambiente():
    """Configura o ambiente inicial do projeto"""
    try:
        # Definir diretórios
        base_dir = Path(__file__).parent
        data_dir = base_dir / 'data'
        
        # Criar diretório de dados se não existir
        data_dir.mkdir(exist_ok=True)
        
        print("\n📁 Configuração do Ambiente")
        print("==========================")
        print(f"\nDiretório base: {base_dir}")
        print(f"Diretório de dados: {data_dir}")
        
        # Listar arquivos necessários
        arquivos_req = [
            'MaturidadeT.xlsx',
            'Alocacao.xlsx', 
            'Executivo.xlsx'
        ]
        
        print("\n📋 Arquivos Necessários:")
        for arquivo in arquivos_req:
            caminho = data_dir / arquivo
            if caminho.exists():
                print(f"✅ {arquivo}: Encontrado")
            else:
                print(f"❌ {arquivo}: Não encontrado")
        
        print("\n🔍 Próximos Passos:")
        print("1. Copie os arquivos Excel para:", data_dir)
        print("2. Execute: python test_insights.py")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro na configuração: {str(e)}")
        return False

if __name__ == "__main__":
    configurar_ambiente()