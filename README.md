<<<<<<< HEAD
# Agente Insights

## Instalação e Configuração

1. Navegue até o diretório do projeto:

```powershell
cd E:\Projeto\Agente_Insights
```

2.Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

3.Instale as dependências:

```powershell
pip install -r requirements.txt
```

4.Verifique a instalação:

```powershell
python -c "import pandas; import numpy; import matplotlib; print('Instalação OK!')"
```

## Estrutura de Arquivos

Certifique-se que os seguintes arquivos estão nos diretórios corretos:

```plaintext
E:\Projeto\Agente_Insights\
├── requirements.txt          # <- Novo arquivo
├── insights.py              # <- Arquivo principal
├── setup_env.py            
└── agenteinsights\
    ├── data\
    │   ├── Alocacao.xlsx
    │   ├── Executivo.xlsx
    │   └── MaturidadeT.xlsx
    └── analise_insights.py
```

## Execução

1. Certifique-se que está no diretório correto e com ambiente virtual ativo:

```powershell
cd E:\Projeto\Agente_Insights
.\.venv\Scripts\activate
```

2.Configure o ambiente:

```powershell
python setup_env.py
```

3.Execute o programa:

```powershell
python insights.py
```
=======
# agente-insights
>>>>>>> 7aa01adfc8dbbb78e5bc1d2fbe8f494c53eed67b
