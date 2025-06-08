
import openai
import os
from dotenv import load_dotenv

# Carregar a chave da API do OpenAI do arquivo .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Configurar a API do OpenAI
openai.api_key = api_key

def iniciar_chat():
    print("Iniciando chat com IA para perguntas sobre os dados...")
    
    # Criar diretório para logs se não existir
    os.makedirs('output/logs', exist_ok=True)
    
    while True:
        pergunta = input("Faça uma pergunta sobre os dados analisados (ou digite 'sair' para encerrar): ")
        
        if pergunta.lower() == 'sair':
            print("Encerrando chat.")
            break
        
        try:
            resposta = openai.Completion.create(
                model="text-davinci-003",
                prompt=pergunta,
                max_tokens=150,
                temperature=0.7
            )
            
            texto_resposta = resposta.choices[0].text.strip()
            print("\nResposta da IA:", texto_resposta)
            
            # Registrar a interação no log
            with open('output/logs/chat_log.txt', 'a', encoding='utf-8') as log_file:
                log_file.write(f"Pergunta: {pergunta}\n")
                log_file.write(f"Resposta: {texto_resposta}\n\n")
                
        except Exception as e:
            print(f"\nErro ao processar a pergunta: {str(e)}")
            # Registrar o erro no log
            with open('output/logs/error_log.txt', 'a', encoding='utf-8') as error_file:
                error_file.write(f"Erro ao processar pergunta '{pergunta}': {str(e)}\n")
