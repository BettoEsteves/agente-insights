"""
Teste de importação de módulo
============================
Script simples para verificar se o módulo está sendo importado corretamente.
"""

import os
import sys

# Verificar o ambiente e caminhos
print(f"Diretório atual: {os.getcwd()}")
print(f"Caminhos de importação Python:")
for path in sys.path:
    print(f" - {path}")

# Tentar importar o módulo
try:
    import agenteinsights
    print(f"\nMódulo importado com sucesso!")
    print(f"Caminho do módulo: {agenteinsights.__file__}")
    print(f"Versão: {getattr(agenteinsights, '__version__', 'Desconhecida')}")
except ImportError as e:
    print(f"\nErro ao importar módulo: {e}")
    print("Verificando diretório do projeto...")
    
    # Listar arquivos e diretórios
    items = os.listdir()
    print("\nArquivos e diretórios encontrados:")
    for item in items:
        if os.path.isdir(item):
            print(f" - {item}/ (diretório)")
        else:
            print(f" - {item} (arquivo)")
