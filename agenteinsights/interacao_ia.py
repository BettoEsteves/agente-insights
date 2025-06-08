import os
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

# Carrega a chave da API do arquivo .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Inicializa o cliente OpenAI
client = OpenAI(api_key=api_key)

def iniciar_chat(dados_cruzados: pd.DataFrame, tribo: str = None):
    """
    Inicia um chat interativo com a IA, utilizando os dados da tribo especificada como contexto.
    Mantém o histórico da conversa para preservar o contexto entre as perguntas.

    Args:
        dados_cruzados: DataFrame com os dados cruzados.
        tribo: Nome da tribo a ser usada como foco da análise. Se None, permite escolher entre todas as tribos.
    """
    print("Iniciando chat com IA para perguntas sobre os dados...")

    # Cria o diretório de logs, se necessário
    os.makedirs('output/logs', exist_ok=True)

    # Identificar todas as tribos únicas
    tribos_unicas = dados_cruzados['tribe'].dropna().unique()
    print(f"Tribos disponíveis: {', '.join(tribos_unicas)}")

    if tribo is None:
        tribo = input("Digite o nome da tribo que deseja analisar: ")

    if tribo not in tribos_unicas:
        print(f"[AVISO] Tribo '{tribo}' não encontrada nos dados.")
        return

    # Filtra os dados da tribo
    dados_tribo = dados_cruzados[dados_cruzados['tribe'].str.lower() == tribo.lower()]

    if dados_tribo.empty:
        print(f"[AVISO] Nenhum dado encontrado para a tribo '{tribo}'.")
        return

    # Gera uma amostra dos dados para fornecer contexto inicial à IA
    contexto_dados = dados_tribo.head(5).to_string(index=False)

    # Histórico da conversa com a IA
    mensagens = [
        {"role": "system", "content": "Você é um analista de dados útil, claro e objetivo."},
        {"role": "user", "content": f"Estes são os dados da tribo '{tribo}':\n\n{contexto_dados}"}
    ]

    while True:
        pergunta = input("\nFaça uma pergunta sobre os dados analisados (ou digite 'sair' para encerrar): ")

        if pergunta.lower() == 'sair':
            print("Encerrando chat.")
            break

        try:
            mensagens.append({"role": "user", "content": pergunta})

            resposta = client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=mensagens,
                temperature=0.7,
                max_tokens=500
            )

            conteudo_resposta = resposta.choices[0].message.content.strip()
            print("\nResposta da IA:", conteudo_resposta)

            mensagens.append({"role": "assistant", "content": conteudo_resposta})

            with open('output/logs/chat_log.txt', 'a', encoding='utf-8') as log_file:
                log_file.write(f"Usuário: {pergunta}\n")
                log_file.write(f"IA: {conteudo_resposta}\n\n")

        except Exception as e:
            print(f"\nErro ao processar a pergunta: {str(e)}")
            with open('output/logs/error_log.txt', 'a', encoding='utf-8') as error_file:
                error_file.write(f"Erro ao processar pergunta '{pergunta}': {str(e)}\n")
