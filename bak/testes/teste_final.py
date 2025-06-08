#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste Final do Agente Insights
==============================
Este script testa se todas as correções foram aplicadas corretamente e
se a tribo Benefícios está sendo analisada corretamente.
"""

import os
import pandas as pd
import logging
import sys
import traceback
from datetime import datetime

# Configurar logging mais detalhado
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        # Adicionar um arquivo de log também
        logging.FileHandler('teste_final.log')
    ]
)

def teste_completo():
    """Testa todas as funcionalidades corrigidas"""
    logging.info(f"{'='*50}")
    logging.info("Iniciando teste final com todas as correções aplicadas...")
    logging.info(f"Data e hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info(f"{'='*50}")
    
    try:
        # Importar funções necessárias
        from agenteinsights.analise_insights import (
            carregar_dados, analisar_alocacao, 
            normalizar_texto, normalizar_nome,
            analisar_cfd, analisar_metricas_ageis
        )
        
        # 1. Testar carregamento de dados
        logging.info("1. Testando carregamento de dados...")
        dados = carregar_dados()
        logging.info(f"Dados carregados. Tipos de dados: {type(dados)}")
        logging.info(f"Chaves no dicionário: {dados.keys() if isinstance(dados, dict) else 'Não é um dicionário'}")
        
        # 2. Testar normalização de texto
        logging.info("2. Testando funções de normalização de texto...")
        textos_teste = ["Benefícios", "BENEFÍCIOS", "beneficios", "  benefícios  ", "benefícios!"]
        for texto in textos_teste:
            resultado = normalizar_texto(texto)
            logging.info(f"Normalização de '{texto}' -> '{resultado}'")
        
        # Verificar compatibilidade com alias
        texto_original = "Benefícios!"
        resultado1 = normalizar_texto(texto_original)
        resultado2 = normalizar_nome(texto_original)
        if resultado1 == resultado2:
            logging.info(f"Alias normalizar_nome funciona corretamente: '{texto_original}' -> '{resultado2}'")
        else:
            logging.error(f"Alias normalizar_nome não está funcionando corretamente!")
        
        # 3. Testar análise de alocação com tribo Benefícios
        logging.info("3. Testando análise de alocação para tribo Benefícios...")
        if 'alocacao' in dados and not dados['alocacao'].empty:
            df_alocacao = dados['alocacao']
            
            # Verificar tribos disponíveis
            tribos = df_alocacao['tribe'].unique()
            logging.info(f"Tribos disponíveis: {tribos}")
            
            # Verificar se a tribo Benefícios existe
            # Usar abordagem case-insensitive para encontrar variações
            tribo_beneficios = None
            for tribo in tribos:
                if normalizar_texto(tribo) == "beneficios":
                    tribo_beneficios = tribo
                    break
            
            if tribo_beneficios:
                logging.info(f"Tribo Benefícios encontrada como: '{tribo_beneficios}'")
                
                # Testar detecção de coluna percentual
                colunas = df_alocacao.columns
                for col in colunas:
                    if col.lower().find("percent") >= 0 or col.lower().find("aloca") >= 0:
                        logging.info(f"Possível coluna de percentual: {col}")
                
                # Executar análise de alocação
                resultado_alocacao = analisar_alocacao(df_alocacao, tribo=tribo_beneficios)
                logging.info(f"Análise de alocação concluída: {len(resultado_alocacao['papeis'])} papéis encontrados")
                
                # Mostrar detalhes da análise
                logging.info(f"Composição de squads: {list(resultado_alocacao['composicao_squads'].keys())}")
                logging.info(f"Alocação média: {resultado_alocacao['alocacao_media']}")
                logging.info(f"Média de pessoas por squad: {resultado_alocacao['media_pessoas_squad']}")
                logging.info(f"Pessoas em múltiplos squads: {resultado_alocacao['pessoas_multi_squad']}")
                
                # 4. Testar análise de métricas
                logging.info("4. Testando análise de métricas ágeis...")
                try:
                    metricas = analisar_metricas_ageis(df_alocacao, tribo=tribo_beneficios)
                    logging.info(f"Métricas ágeis: {metricas}")
                    
                    if 'throughput_diario' in metricas:
                        logging.info(f"Throughput diário: {metricas['throughput_diario']}")
                    else:
                        logging.warning("Throughput diário não encontrado nas métricas")
                        
                except Exception as e:
                    logging.error(f"Erro na análise de métricas: {str(e)}")
                    traceback.print_exc()
                    return False
            else:
                logging.error(f"Tribo Benefícios não encontrada. Tribos disponíveis: {tribos}")
                return False
        else:
            logging.error("Dados de alocação não disponíveis")
            return False
            
        logging.info(f"{'='*50}")
        logging.info("Teste final concluído com sucesso!")
        logging.info(f"{'='*50}")
        return True
        
    except Exception as e:
        logging.error(f"Erro no teste final: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    sucesso = teste_completo()
    if sucesso:
        print("Teste final concluído com sucesso!")
        sys.exit(0)
    else:
        print("Teste final falhou")
        sys.exit(1)
