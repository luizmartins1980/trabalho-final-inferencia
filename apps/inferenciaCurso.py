import zipfile
import streamlit as st
import pandas as pd
import statistics 
import scipy.stats
import numpy as np
import matplotlib.pyplot as plt


def inferenciaCurso():

    # print usando markdown
    st.markdown("# **Trabalho final inferência estatística**")

    # print usando markdown
    st.markdown("---")

    # lendo a base de dados
    with zipfile.ZipFile("./data/BaseTratada.zip") as zip:
        with zip.open("BaseTratada.csv") as arq:
            dfBase = pd.read_csv(arq, delimiter=";",
                                 decimal=",",  encoding="ISO-8859-1")

    # alterando o tipo de dados das notas
    dfBase = dfBase.astype({"NotaGeral": "float64",
                            "NotaConhGeral": "float64",
                            "NotaConhEspecifico": "float64"})


    #criando função para o intervalo de confiança
    def intervalo_confianca(x_barra:float, amostra:int, confianca:float, sigma:float):
        """Calcula o intervalo de confiança em uma normal.

        Args:
            x_barra (float): média amostral
            amostra (int): tamanho da amostra
            confianca (float): confiança desejada
            sigma (float): sigma

        Returns:
            list: intervalo de confiança
        """
        
        # atribuindo valor Z alpha conforme nivel confiança
        zalpha = abs(scipy.stats.norm.ppf((1 - confianca)/2.))
        
        #calculando intervalo 1
        IC1 = x_barra - zalpha*sigma/np.sqrt(amostra)

        #calculando intervalo 2
        IC2 = x_barra + zalpha*sigma/np.sqrt(amostra)

        #retornando intervalos
        return [IC1, IC2]


    # questão A - print usando markdown
    questao = """
                ***A) Faça a importação para o Colab do arquivo do ENADE 2017 Utilizado em nosso curso (MICRODADOS_ENADE_2017.txt)***

                ***Resposta:*** Foi utilizada a base do ENADE 2109. A importação pode ser observada durante a execução do trablho ou no menu Tratamento Base. 
              """
    st.markdown(questao)
    
    # print usando markdown
    st.markdown("---")

    # questão B - print usando markdown
    questao = """
                ***B) Faça as estatísticas descritivas do seu banco (Resumo geral), avaliando se há variáveis faltantes ou não, e se existirem, elimine-as.***

                ***Resposta:*** As estatísticas descritivas podem ser visualizadas no menu Análise por Curso. Quanto ao tratamento das variáveis, estes 
                tratamentos podem ser observados no menu Tratamento Base. 
              """
    st.markdown(questao)

    # print usando markdown
    st.markdown("---")
    
    # questão C - print usando markdown
    st.markdown("***C) Utilize a variável NT_GER para calcular a média geral das notas dos alunos de todos os cursos do ENADE.***")
    #calculando a média
    st.markdown("***Resposta:***")
    st.text("")
    
    #calculando o desvio
    desvioPopulacional =  round(statistics.stdev(dfBase["NotaGeral"]),3)

    #calculando a média
    mediaGeral = round(dfBase["NotaGeral"].mean(),3)

    #criando colunas para mostrar respostas
    col1, col2 = st.columns(2)

    #coluna 1 - média
    with col1:
        st.metric("Média Geral",mediaGeral)
    
    #coluna 2 - desvio
    with col2:
        st.metric("Desvio Padrão", desvioPopulacional)
    
    # print usando markdown
    st.markdown("---")
    
    #questões D, E, F, H - print usando markdown
    questao = """
                ***D) Escolha um  curso a sua escolha, calculando a  média de notas de alunos do mesmo.***
                
                ***E) Calcule o desvio padrão amostral das notas dos alunos do curso escolhido.***
                
                ***F) Calcule o intervalo de confiança(IC) ao nível de confiança de 95% para a média populacional 
                das notas do curso escolhido e o interprete corretamente.***

                ***H) Segundo o IC calculado em F), você diria que a nota dos alunos do curso escolhido em D) foi atípica ou não?***

                ***Resposta:***
              """
    st.markdown(questao)

    #criando listas para a tabela
    nomeCurso, mediaNota, desvioAmostral, tamanhoAmostra, intervalo1, intervalo2, estudo = [], [], [], [], [], [], []

    #for nos cursos existentes na base
    for curso in  sorted(dfBase["Curso"].unique().tolist()):

        #filtrando a base para o curso
        dfBaseFiltrada = dfBase[dfBase["Curso"] == curso]
        
        #calculando média da nota do curso
        mediaCurso = dfBaseFiltrada["NotaGeral"].mean()

        #tamanho da amostra
        n = len(dfBaseFiltrada)
        
        #calculando o intervalo de confiança
        intervalo = intervalo_confianca(x_barra= mediaCurso, amostra= n, confianca= 0.95, sigma= desvioPopulacional)

        #alimentando listas
        nomeCurso.append(curso)
        tamanhoAmostra.append(n)
        mediaNota.append(mediaCurso)
        desvioAmostral.append(round(statistics.stdev(dfBaseFiltrada["NotaGeral"]),3)) 
        intervalo1.append(intervalo[0])
        intervalo2.append(intervalo[1])

        #atípica ou não
        if intervalo[0] <= mediaGeral <= intervalo[1]:
            estudo.append("Não")
        else:
            estudo.append("Sim")

    #mostrando tabela
    st.table({"Curso" : nomeCurso, "Tamanho Amostra":tamanhoAmostra, "Média Nota":mediaNota, "Desvio Amostra":desvioAmostral, "Intervalo1" :intervalo1, "Intervalo2" :intervalo2, "Nota Atípica" :estudo})

    #print usando mardown
    st.markdown("Nos intervalos obtidos contém a média das notas com a confiança de 95%.")
    st.markdown("---")

    #questão G - print usando markdown
    questao = """
                ***G) Qual a distribuição será aplicada para encontrar os quantis das notas do curso escolhido em D) e diga o porquê da escolha da mesma.***

                ***Resposta:*** A distribuição utilizada foi a Normal, visto que, todas as amostras possuem mais do que 30 elementos e com sigma conhecido.
              """
    st.markdown(questao)
    st.markdown("---")

    #questão H
    questao = """
                I) Faça um teste de hipótese bilateral ao nível de confiança de 95% para média das notas do curso escolhido, verifique se a razão para dizer
                 que a média das notas do curso escolhido é significativamente diferente da média geral das notas do enade, ao nível de confiança de 95%.

                ***Resposta:*** 
              """
    st.markdown(questao)


    for curso in  sorted(dfBase["Curso"].unique().tolist()):
        
        #print título do curso
        st.markdown(f"## {curso}")
        
        #filtrando a base para o curso
        dfBaseFiltrada = dfBase[dfBase["Curso"] == curso]

        #média do curso observado
        xobs = dfBaseFiltrada["NotaGeral"].mean()

        #definindo alpha
        alpha = 5

        #calculando os percentis
        xc1 = np.percentile(dfBase["NotaGeral"], alpha)
        xc2 = np.percentile(dfBase["NotaGeral"], 100-alpha)
        
        #verificando o xobs para saber se entcotra dentro do intervalo
        if(xobs < xc1 or xobs > xc2):
            st.write("É significativamente diferente da média geral")
        else:
            st.write("Não é significativamente diferente da média geral")

        #plotando gráfico
        fig = plt.figure(figsize=(8,4))
        plt.hist(x=dfBase["NotaGeral"], bins=20, color="blue", alpha=0.7, rwidth=0.85, density=True)
        plt.axvline(x=xc1, color="red", linestyle="--", label = "xc1")
        plt.axvline(x=xc2, color="red", linestyle="--", label = "xc2")
        plt.axvline(x=xobs, color="black", linestyle="--", label = "xobs")
        plt.legend()
        st.pyplot(fig)