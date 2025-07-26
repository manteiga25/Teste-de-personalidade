from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import winsound
import random
import os
import sys
from validate_email import validate_email
import threading
from PIL import Image, ImageTk
import requests
import xml.etree.ElementTree as ET
import time
from time import gmtime, strftime
import psycopg2
import smtplib
from email.mime.text import MIMEText

diretorio_g = ""
diretorio_audio = ""
diretorio_audio_b = ""

def enviar_email(nome, email, resultado, data, texto) -> None:
    servidor = smtplib.SMTP('smtp.gmail.com', 587)
    servidor.starttls()
    servidor.login('mentescriativas117@gmail.com', '')
    global idioma
    if idioma == "PT":
        assunto = 'Resultado do teste de personalidade'
        corpo = "Olá " + nome + ", o resultado do seu teste de personalidade realizado no dia " + str(data) + " foi " + resultado + ".\n" + texto
    else:
        assunto = 'Result of personality test'
        corpo = "Hi " + nome + ", the result of your personality test realized on " + str(data) + " is " + resultado + ".\n" + texto

    msg = MIMEText(corpo)
    msg['From'] = 'mentescriativas117@gmail.com'
    msg['To'] = email
    msg['Subject'] = assunto

    servidor.sendmail('mentescriativas117@gmail.com', email, msg.as_string())
    servidor.quit()

def inicializa_diretorio() -> None:
    diretorio_de_dados = os.path.join(os.getenv('APPDATA'), 'Teste_de_personalidade')

    # Cria o diretório se não existir
    if not os.path.exists(diretorio_de_dados):
        os.makedirs(diretorio_de_dados)

    os.chdir(diretorio_de_dados)

def conectar_banco_de_dados() -> psycopg2.extensions.connection:
    # Conecte-se ao banco de dados remoto
    conexao = psycopg2.connect(
        host="surus.db.elephantsql.com",
        port=None,
        user="tgzkwyzy",
        password="pMRrG6CmTqWzwtXGWPsj3R9ohD82OXf6",
        database="tgzkwyzy"
    )
    return conexao


def inserir_usuario(nome, email, resultado, data) -> None:
    conexao = conectar_banco_de_dados()
    cursor = conexao.cursor()

    comando_sql = '''
        INSERT INTO testes (nome, email, resultado, data) 
        VALUES (%s, %s, %s, %s)
    '''
    
    # Executa o comando SQL para inserir um novo usuário
    cursor.execute(comando_sql, (nome, email, resultado, data))

    # Confirma a transação e fecha a conexão
    conexao.commit()
    cursor.close()
    conexao.close()

def receber_dados() -> list:
    conexao = conectar_banco_de_dados()
    cursor = conexao.cursor()
    
    # Executa o comando SQL para inserir um novo usuário
    cursor.execute("SELECT resultado FROM testes")
    dados_res = cursor.fetchall()
    cursor.close()
    conexao.close()
    return dados_res

#Variavel Global do programa todo
idioma = 'PT'
fich_async = winsound.SND_FILENAME | winsound.SND_ASYNC
mudou = False

# se o ficheiro não existir cria um ficheiro e coloca o idioma português por padrão
def detectar_idioma_padrao() -> None:
    global idioma
    if not os.path.exists("Idioma.txt"):
        idioma_fd = open("Idioma.txt", "w")
        idioma_fd.write("PT")
    else:
        idioma_fd = open("Idioma.txt", "r")
        if idioma_fd.read() == "IN":
            idioma = 'IN'
    idioma_fd.close()

def escrever_idioma(idioma_str) -> None:
    esc_idi = open("Idioma.txt", "w") # não á problema em recriar o ficheiro
    esc_idi.write(idioma_str)
    esc_idi.close()

class tipos_personalidade:

    # lista com as respostas
    resp = list(range(12))
    fase_2_resp = list(range(4))
    fase_2_1_resp = list(range(2))

    nome_text = ""

    # variaveis fase cinzento
    tipo_cinzento_str = ['' for _ in range(10)]
    
    # variaveis fase rosa
    tipo_rosa_str = ['' for _ in range(10)]

    # variaveis fase azul
    tipo_azul_str = ['' for _ in range(10)]

    # resultado
    resultado_str = ['' for _ in range(10)]

    inf_personalidade_str = ['' for _ in range(10)]

    caminho_img_fundo_init_str = ""

    caminho_img_botoes_str = ['' for _ in range(5)]

    caminho_img_fundo_str = ['' for _ in range(10)]

    caminho_img_fundo_str[0] = ""
    caminho_img_fundo_str[1] = diretorio_g + "perfecionista.png"
    caminho_img_fundo_str[2] = diretorio_g + "prestativo.png"
    caminho_img_fundo_str[3] = diretorio_g + "Bem-sucedido.png"
    caminho_img_fundo_str[4] = diretorio_g + "Individual.png"
    caminho_img_fundo_str[5] = diretorio_g + "Observador.png"
    caminho_img_fundo_str[6] = diretorio_g + "Questionador.png"
    caminho_img_fundo_str[7] = diretorio_g + "Sonhador.png"
    caminho_img_fundo_str[8] = diretorio_g + "Confrontador.png"
    caminho_img_fundo_str[9] = diretorio_g + "Pacifista.png"

    # return 0 se idioma for o mesmo
    def verificar_idioma(self, idioma_str) -> bool:
        idioma_sel = idioma_str.get()
        global mudou
        global idioma
        if idioma_sel == idioma:
            mudou = False
            return 0
        else:
            if idioma_sel == "IN":
                pergunta_idioma = tk.messagebox.askquestion("Mudar Idioma", "Tem certeza que quer mudar o idioma?")
            else:
                pergunta_idioma = tk.messagebox.askquestion("Switch Language", "Are you sure you want to change the language?")
            if pergunta_idioma == "no":
                return 1
            self.mudar_idioma(idioma_sel)
            escrever_idioma(idioma_sel)
            mudou = True

    def mudar_idioma(self, idioma_str) -> None:
        global idioma
        idioma = idioma_str
        # Não faz nada se for o mesmo idioma, vai ser util para o futuro
        if idioma_str == "PT":

            self.nome_text = "Nome:"
    
            self.caminho_img_fundo_init_str = diretorio_g + "fundo_init.png"

            self.caminho_img_botoes_str[0] = diretorio_g + "botao_f.png"
            self.caminho_img_botoes_str[1] = diretorio_g + "reg.png"
            self.caminho_img_botoes_str[2] = diretorio_g + "idioma.png"
            self.caminho_img_botoes_str[3] = diretorio_g + "menu.png"
            self.caminho_img_botoes_str[4] = diretorio_g + "mais.png"

            self.tipo_cinzento_str[0] = ""
            self.tipo_cinzento_str[1] = "Perfeccionismo, Disciplinado, Foco no detalhe Rígido e determinado"
            self.tipo_cinzento_str[2] = "Empenhado, Habilidade nas relações, Organizado, Voluntarioso"
            self.tipo_cinzento_str[3] = "Competitivo, Confiante, Foco no sucesso, Objetivo"
            self.tipo_cinzento_str[4] = "Sonhador, Intenso, Emotivo, Romântico"
            self.tipo_cinzento_str[5] = "Analítico, Observador, Frio Emocionalmente, Independente"
            self.tipo_cinzento_str[6] = "Questionador, Precavido, Organizado, Antecipa os vários cenários"
            self.tipo_cinzento_str[7] = "Otimista, Entusiasta, Criativo, Foco em multi-opções"
            self.tipo_cinzento_str[8] = "Direto, Frontal, Impaciente com ritmo de outros, Assertivo"
            self.tipo_cinzento_str[9] = "Pacificador, Flexível, Calmo e cordial, Dificuldade em dizer não"

            self.tipo_rosa_str[0] = ""
            self.tipo_rosa_str[1] = "Os outros veem-me como perfeccionista, Disciplina e rigor são importantes para mim"
            self.tipo_rosa_str[2] = "Os outros veem-me como disponível, Conexão com os outros e ajudar é importante para mim"
            self.tipo_rosa_str[3] = "Os outros veem-me como alguém bem sucedido, O resultado e o reconhecimento são importantes para mim"
            self.tipo_rosa_str[4] = "Os outros veem-me como alguém diferente, Sentir-me especial é importante para mim"
            self.tipo_rosa_str[5] = "Os outros veem-me como alguém frio e distante, Conhecimento e isolamento são importantes para mim"
            self.tipo_rosa_str[6] = "Os outros veem-me como alguém desconfiado, Antecipação de cenários é importantepara mim"
            self.tipo_rosa_str[7] = "Os outros veem-me como alguém entusiasta, Ter planos e várias opções é importante para mim"
            self.tipo_rosa_str[8] = "Os outros veem-me como alguém demasiado frontal, Controlo é importante para mim"
            self.tipo_rosa_str[9] = "Os outros veem-me como alguém flexível, Harmonia éimportante para mim"

            self.tipo_azul_str[0] = ""
            self.tipo_azul_str[1] = "Foco no acerto e errado, Alto nível de exigência, Foco no detalhe e no rigor"
            self.tipo_azul_str[2] = "Foco em ajudar os outros,  Fácil comunicar e relacionar, Proatividade na ajuda aos outros"
            self.tipo_azul_str[3] = "Foco nas metas e concretização, Vaidade pelas suas conquistas, Foco na imagem e performance"
            self.tipo_azul_str[4] = "Preocupação em ser diferente, Intensidade emocional, Muito exigenteconsigo mesmo"
            self.tipo_azul_str[5] = "Foco na sua privacidade, Prazer pelo isolamento, Frieza, lógica e racionalidade"
            self.tipo_azul_str[6] = "Foco em antecipar, Dificuldade em confiar, Hábil em fazer questões"
            self.tipo_azul_str[7] = "Foco em manter varias opções, Entusiasmo e criatividade, Otimismo e foco no prazer"
            self.tipo_azul_str[8] = "Foco em manter o controlo, Frontalidade e assertividade, Justiça e defesa dos mais fracos"
            self.tipo_azul_str[9] = "Foco na harmonia e consenso, Dificuldade em dizer não, Flexibilidade em aceitar os outros"

            self.resultado_str[0] = ""
            self.resultado_str[1] = "Perfecionista"
            self.resultado_str[2] = "Prestativo"
            self.resultado_str[3] = "Bem-sucedido"
            self.resultado_str[4] = "Romantico"
            self.resultado_str[5] = "Frio"
            self.resultado_str[6] = "Questionador"
            self.resultado_str[7] = "Sonhador"
            self.resultado_str[8] = "Confrontador"
            self.resultado_str[9] = "Pacificador"

            self.inf_personalidade_str[0] = ""
            self.inf_personalidade_str[1] = "“Trabalho arduamente para restabelecer a perfeição. As regras são para cumprir e o dever vem em primeiro lugar.\nNum papel de liderança defino objetivos claros e inspiro os outros a atingir altos standards de qualidade. Sou extremamente exigente com as minhas equipas e em particular com aqueles em que mais confio.\n\nSou sem dúvida uma pessoa extremamente determinada, organizada, responsável e trabalhadora focada na criação de mecanismos para melhoria contínua, buscando a excelência.\nO exagero dos nossos talentos revela os nossos pontos fracos, por isso sou também uma pessoa inflexível, excessivamente exigente e excessivamente preocupada.”\n\nEntre em acção com algumas dicas de crescimento:\nAinda que lhe pareça estranho e naturalmente menos fácil, desafie-se a fazer algo imperfeito ou de uma forma um pouco mais relaxada.\nAprenda a aceitar os seus erros e a apreciar-se tal como é.\nE, já agora, uma vez por outra, permita-se perder “completamente” o controlo e volte mais aliviado."
            self.inf_personalidade_str[2] = "“Sou uma pessoa prestativa, disponível e antecipo-me a ajudar os que considero que precisam de mim.\nTenho uma grande facilidade no relacionamento interpessoal e num papel de liderança tenho tendência a desenvolver equipas muito próximas, que se protegem e se apoiam contudo, sinto uma grande dificuldade em pedir ajuda e em dizer NÃO às pessoas que me são especiais passando assim as minhas necessidades/vontades para 2º plano.\nSou sem dúvida uma pessoa empática, voluntariosa, generosa, empenhada e atenta aos outros.\nO exagero dos nossos talentos revela os nossos pontos fracos, por isso sou também uma pessoa teimosa, indireta e tenho momentos em que me sinto carente de atenção.”\n\nEntre em acção com algumas dicas de crescimento:\nContrarie o querer fazer tudo.\nFaça uso da sua criatividade. Mesmo que aparentemente lhe falte tempo, contrarie-se.\nObserve-se mais.\nObrigue-se a fazer coisas a sós, a entrar mais em contacto com a natureza e em relaxar."
            self.inf_personalidade_str[3] = "“Sou uma pessoa focada numa imagem de sucesso, dedicada e eficiente.\nNum papel de liderança tenho tendência a criar um ambiente que atinja resultados e que seja altamente focado nas metas.\n\nSou sem dúvida uma pessoa determinada e extremamente focada em objetivos e resultados.\nVivo a minha vida a um ritmo claramente mais acelerado que os outros.\nTenho uma habilidade única a negociar, como se estivesse equipado com um sonar especial.\nO exagero dos nossos talentos revela os nossos pontos fracos, por isso sou também uma pessoa impaciente, excessivamente competitiva e autocentrada.”\n\nEntre em acção com algumas dicas de crescimento:\nProcure diminuir o seu ritmo. Se não for muito fácil, defina isso como objetivo e comece com pequenas metas. Atingir objetivos continua, afinal, a ser algo natural e fácil para si.\nSinta os que mais gosta. Permita-se emocionar.\nDa próxima vez que for de férias, defina um horário para ter acesso ao seu mundo profissional. Defina isso como meta e não se deixe vencer.\nEste foi apenas o levantar da ponta do véu…\nAgora a DICA DE OURO que pode mudar a sua VIDA como mudou a MINHA.\n\nVocê acredita que relacionamentos mais equilibrados podem melhorar a sua vida?\n\nQuando nos conhecemos a nós mesmos e aos outros, somos mais tolerantes e as nossas relações melhoram. E isso tem impacto na nossa auto-estima, confiança e felicidade."
            self.inf_personalidade_str[4] = "“Sou uma pessoa que se aperfeiçoa e procura fazer tudo de uma forma única, especial e talvez até romântica.\nNum papel de liderança dou às pessoas significado e propósito para que elas possam mostrar toda a sua inspiração e excelência.\n\nSou sem dúvida uma pessoa criativa, incentivadora, idealista, expressiva e empenhada em criar ambientes competitivos mas com alto nível de envolvimento das pessoas e das equipas.\n\nO exagero dos nossos talentos revela os nossos pontos fracos, por isso sou também uma pessoa instável, queixosa e receoso/a de perder relações.”\n\nEntre em acção com algumas dicas de crescimento:\nFique atento às comparações. Aperceba-se do quanto se compara com as outras pessoas. Compreenda que essa comparação alimenta a sua instabilidade.\nEntenda as emoções como uma ferramenta de aprendizagem. Procure tirar prazer de coisas simples e valorizar o que tem e não o que não tem.\nFaça por viver o presente."
            self.inf_personalidade_str[5] = "“Sou uma pessoa que precisa de se resguardar para, em privado, poder pensar, informar-me e recarregar as minhas baterias.\nNum papel de liderança desenvolvo uma organização eficiente através do uso de planeamento, critério para que todos trabalhem com uma missão comum.\n\nSou sem dúvida uma pessoa, lógica, analítica, calma nas crises, que compreende o ambiente como invasivo e procuro preservar os meus recursos mais valiosos, como tempo, informação e energia, através da defesa exagerada da minha privacidade.\n\nA minha visão extremamente racional e objetiva proporcionam uma substancial capacidade de definir critérios, métodos e planeamento de longo prazo.\n\nO exagero dos nossos talentos revela os nossos pontos fracos, por isso sou também uma pessoa distante, reservada e contida nas relações.”\n\nEntre em acção com algumas dicas de crescimento:\nPonha o seu corpo a funcionar, praticando regularmente atividades físico-desportivas. Somos mais do que pensamentos.\nHabitue-se a circular um pouco mais pelo seu local de trabalho e a fazer alguma conversa de circunstância."
            self.inf_personalidade_str[6] = "“Sou uma pessoa que considera que nem mesmo a autoridade é confiável, por isso, testo-a e questiono-a.\n\nNum papel de liderança tenho tendência a resolver problemas da organização e desenvolver um ambiente em que cada pessoa sinta que é parte da solução.\n\nSou sem dúvida uma pessoa estratega, criteriosa, cautelosa e que antecipa facilmente cenários negativos, extremamente eficaz no planeamento e comprometida.\nO exagero dos nossos talentos revela os nossos pontos fracos, por isso sou também uma pessoa insegura, ansiosa e desconfiada.”\n\nEntre em acção com algumas dicas de crescimento:\nIdentifique os seus receios. A identificação é o primeiro passo para a transformação.\nControle o seu ritmo e ansiedade. Ponha por escrito os seus pensamentos nos momentos em que sente maior ansiedade. Volte a lê-los mais tarde e compreenda o que lhe ensinam sobre si."
            self.inf_personalidade_str[7] = "“Sou uma pessoa otimista, criativa e entusiasmada por novas ideias, experiências, projetos e pessoas.\n\nNum papel de liderança gosto de ter as pessoas entusiasmadas e motivá-las a criar inovações que deem vantagem competitiva na conquista de oportunidades.\n\nSou sem dúvida uma pessoa bem-humorada, espontânea, curiosa, produtiva e com enorme capacidade de síntese.\nO exagero dos nossos talentos revela os nossos pontos fracos, por isso sou também uma pessoa anti rotina, descomprometida e dispersa.”\n\nEntre em acção com algumas dicas de crescimento:\nAprenda a lidar com limitações. Quando surgir a ansia de seguir para um novo projeto ou ideia, respire fundo e procure acabar o que ainda tem em mãos.\nDiminua as suas opções. Em vez de aumentar a pressão com os outros, procure diminuir os seus focos de atenção.\nFundamentalmente, compreenda que, na vida, tudo tem um ritmo e um momento para acontecer."
            self.inf_personalidade_str[8] = "“Sou uma pessoa que repõe a justiça e luto para defender os inocentes e desprotegidos porque são mais frágeis.\n\nNum papel de liderança gosto de mover a organização liderando assertivamente e tendo equipas determinadas em agir e conquistar.\n\nSou sem dúvida uma pessoa dinâmica, eficaz, decidida e que aceita tomar por sua conta e risco os desafios com que me cruzo.\n\nO exagero dos nossos talentos revela os nossos pontos fracos, por isso sou também uma pessoa impaciente, exagerada e autoritária.”\n\nEntre em acção com algumas dicas de crescimento:\nRespeite os seus limites. Fique atento ao seu ritmo e aprenda a escutar o seu corpo.\nNão despreze o seu lado mais sensível. Ele é compatível com assertividade e determinação. Por último, lembre-se de que é um ser humano. Quando as suas fragilidades ocorrerem, não as disfarce, aprenda com elas."
            self.inf_personalidade_str[9] = "“Sou uma pessoa que está em paz quando todos á minha volta estão bem e unidos.\n\nNum papel de liderança gosto de Viver a missão da organização promovendo um ambiente harmonioso e estruturado.\n\nSou sem dúvida uma pessoa com afável, flexível e com uma notável capacidade diplomática e uma cordialidade carismática.\n\nO exagero dos nossos talentos revela os nossos pontos fracos, por isso sou também uma pessoa teimosa, indecisa e apática.”\n\nEntre em acção com algumas dicas de crescimento:\nSorria menos. Apareça mais e não tema ter destaque. Insista na colocação dos seus pontos de vista e interesses em cima da mesa.\nDe tempos a tempos, atreva-se a ter uma discussão mais acesa. Vai ver que o mundo não acaba. Pratique desporto ou uma atividade física regular.\nFaça listas de tarefas a executar em cada dia para compreender o quanto se esquece dos seus objetivos e procure contrariar a situação. Não se esqueça de verificar a lista."
        else:

            self.nome_text = "Name:"

            self.caminho_img_fundo_init_str = diretorio_g + "fundo_init_ing.png"

            self.caminho_img_botoes_str[0] = diretorio_g + "botao_init_ing.png"
            self.caminho_img_botoes_str[1] = diretorio_g + "reg_ing.png"
            self.caminho_img_botoes_str[2] = diretorio_g + "idioma_ing.png"
            self.caminho_img_botoes_str[3] = diretorio_g + "botao_menu_ing.png"
            self.caminho_img_botoes_str[4] = diretorio_g + "mais_ing.png"

            self.tipo_rosa_str[0] = ""
            self.tipo_rosa_str[1] = "Others see me as a perfectionist, Discipline and rigor are important to me"
            self.tipo_rosa_str[2] = "Others see me as available, Connection with others and helping is important to me"
            self.tipo_rosa_str[3] = "Others see me as someone successful, Results and recognition are important to me"
            self.tipo_rosa_str[4] = "Others see me as someone different, Feeling special is important to me"
            self.tipo_rosa_str[5] = "Others see me as cold and distant, Knowledge and isolation are important to me"
            self.tipo_rosa_str[6] = "Others see me as suspicious, Anticipating scenarios is important to me"
            self.tipo_rosa_str[7] = "Others see me as enthusiastic, Having plans and several options is important to me"
            self.tipo_rosa_str[8] = "Others see me as someone who is too frontal, Control is important to me"
            self.tipo_rosa_str[9] = "Others see me as flexible, Harmony is important to me"

            self.tipo_azul_str[0] = ""
            self.tipo_azul_str[1] = "Focus on right and wrong, High level of demand, Focus on detail and rigor"
            self.tipo_azul_str[2] = "Focus on helping others, Easy to communicate and relate, Proactivity in helping others"
            self.tipo_azul_str[3] = "Focus on goals and achievement, Vanity for your achievements, Focus on image and performance"
            self.tipo_azul_str[4] = "Concern about being different, Emotional intensity, Very demanding of oneself"
            self.tipo_azul_str[5] = "Focus on your privacy, Pleasure for isolation, Coldness, logic and rationality"
            self.tipo_azul_str[6] = "Focus on anticipating, Difficulty trusting, Skilled in asking questions"
            self.tipo_azul_str[7] = "Focus on maintaining multiple options, Enthusiasm and creativity, Optimism and focus on pleasure"
            self.tipo_azul_str[8] = "Focus on maintaining control, Frontality and assertiveness, Justice and defense of the weakest"
            self.tipo_azul_str[9] = "Focus on harmony and consensus, Difficulty saying no, Flexibility in accepting others"

            self.resultado_str[0] = ""
            self.resultado_str[1] = "Perfectionist"
            self.resultado_str[2] = "Helpful"
            self.resultado_str[3] = "Successful"
            self.resultado_str[4] = "Romantic"
            self.resultado_str[5] = "analytical"
            self.resultado_str[6] = "Questioner"
            self.resultado_str[7] = "Dreamer"
            self.resultado_str[8] = "Confrontational"
            self.resultado_str[9] = "Controller"

            self.inf_personalidade_str[0] = ""
            self.inf_personalidade_str[1] = "The first of the enneatypes is characterized by an ego that is very focused on discipline, it always seeks to highlight the errors in everything it sees and is incapable of leaving a detail unaddressed.\nThey are orderly and have a very strong conception of what is right and what is wrong.\nDespite their good intentions, in their search for perfection, they can hurt other people's feelings by always highlighting the negative details.\nThe ONE's psychological work will be based on finding peace, being less self-demanding, cultivating kindness, accept yourself and others."
            self.inf_personalidade_str[2] = "People of this enneatype focus all their attention on others, seek love through acts or gestures of helping others and generally feel a type of ""pride"" when they feel that someone needs them.\nThey want to be loved and feel wanted at a cost that is needed.\nThey do not focus on their needs and this can affect their personal well-being.\nThe growth objective of a TWO will be to learn to give love and stop needing external affection, recognize their humility and let it go brings a feeling of pride."
            self.inf_personalidade_str[3] = "Type THREE is characterized by a tendency to act as he or she believes others want him or her to act.\nThey care greatly about the image they project to others and live by and for it.\nThe path to good- Being a THREE will be guided to leave vanity behind and act according to their own feelings and emotions, ceasing to focus on what others think."
            self.inf_personalidade_str[4] = "These people connect deeply with emotions, they have a strong unconscious need to feel loved, to be unique and special.\nThey often develop disorders related to depression and have a deep feeling of inferiority.\nThey are the most creative personality type, but at the same time more melancholic and pessimistic.\nPsychological advice for an individual with a FOUR personality will be focused on cultivating a feeling of equality in relation to others, self-esteem and letting oneself be loved."
            self.inf_personalidade_str[5] = "Those analytical, observant and perceptive people are generally described as personality type FIVE.\nTheir world is in their head and they rarely share it, they have a deep difficulty connecting with emotions and even more so if they are foreigners.\nThe path to The growth of a person with an enneatype FIVE will be directed away from personal isolation and sharing their thoughts and emotions with others."
            self.inf_personalidade_str[6] = "Individuals who are defined as enneatype SIX are those whose main value is sincerity and fidelity.\nThey are generally extremely anxious and suspicious, they are afraid of the unknown and everything that can cause some type of emotional harm.\nThe emotional goals of the SIX will be find the value within them and learn to trust their attitudes."
            self.inf_personalidade_str[7] = "Active, lively, distracted... the SEVEN are an enneatype full of energy and desire for freedom.\nThey are people who escape routine by making a thousand plans to distract themselves, constantly seek new and satisfying experiences and generally live under a mask of joy to avoid connecting with pain and reality when it is not pleasant.\nThe psychological tip that type SEVEN can improve will be based on taking responsibility, emotional maturity and connection with reality."
            self.inf_personalidade_str[8] = "Type EIGHT personalities are characterized by strong control over their environment and the desire to hide their weaknesses at all costs.\nThey are combative, aggressive and power-oriented people.\nThey seek to protect those individuals who they consider ""deserving of protection "" and try to impose their ideas at all costs.\nFor an EIGHT to grow emotionally, work aimed at recovering the innocence and kindness of the inner child, accepting their weaknesses and learning to live in love is recommended."
            self.inf_personalidade_str[9] = "People of this enneatype are calm, mediating individuals with a tendency to avoid conflict.\nThey need peace and harmony to reign in their environment.\nThey generally do not confront others because they do not want to break this internal tranquility, which is why they They feel uncomfortable with changes and unexpected challenges.\nThe recommended goals for personality type NINE will be related to showing your emotions, learning to make decisions and loving yourself, respecting your real desires."

            self.tipo_cinzento_str[0] = ""
            self.tipo_cinzento_str[1] = "Perfectionism, Disciplined, Focus on detail Rigid and determined"
            self.tipo_cinzento_str[2] = "Committed, Relationship skills, Organized, Voluntary"
            self.tipo_cinzento_str[3] = "Competitive, Confident, Focus on success, Objective"
            self.tipo_cinzento_str[4] = "Dreamy, Intense, Emotional, Romantic"
            self.tipo_cinzento_str[5] = "Analytical, Observant, Emotionally Cold, Independent"
            self.tipo_cinzento_str[6] = "Questioning, Cautious, Organized, Anticipates various scenarios"
            self.tipo_cinzento_str[7] = "Optimistic, Enthusiastic, Creative, Focus on multi-options"
            self.tipo_cinzento_str[8] = "Direct, Frontal, Impatient with others' pace, Assertive"
            self.tipo_cinzento_str[9] = "Peacemaker, Flexible, Calm and cordial, Difficulty saying no"

class App:

    global diretorio_audio_b

    def cria_xml(self):
        cria = True
        if os.path.exists('resultado.xml'):
            try:
        # Se existir, carregue o arquivo XML existente
                tree = ET.parse('resultado.xml')
                self.dados = tree.getroot()
                cria = False
            except:
                if idioma == "PT":
                    tk.messagebox.showerror("Erro de escrita", "Foi detectado uma possível violação no ficheiro de registro do programa.", detail="O ficheiro sera recriado.")
                else:
                    tk.messagebox.showerror("Write error", "A possible violation has been detected in the program's log file.", detail="The file will be recreated.")
        if cria:
        # Se não existir, crie um novo elemento raiz
            self.dados = ET.Element("dados")
            tree = ET.ElementTree(self.dados)
        return tree

    def escreve_resultado_xml(self, fich_obj, resultado_index, resultado) -> None:
        novo_elemento = ET.SubElement(fich_obj, resultado_index)
        for key, value in resultado.items():
            esc_resultado = ET.SubElement(novo_elemento, key)
            esc_resultado.text = str(value)

    def le_registro_xml(self) -> list:
        fich_le_xml = ET.parse('resultado.xml')
        const_dados = fich_le_xml.getroot()
        numero_de_dados = len(list(const_dados))
        const_dados_formatados = [['' for _ in range(4)] for _ in range(numero_de_dados)]
        for linha in range(len(list(const_dados))):
            for coluna in range(4):
                const_dados_formatados[linha][coluna] = const_dados[linha][coluna].text
        return const_dados_formatados

    def mostrar_info(self, inf_personalidade, tit_personalidade, img_path) -> None:
        self.botao_info["state"] = "disabled"
        self.botao_menu["state"] = "disabled"
        janela_info = Toplevel(self.janela_init)
        janela_info.protocol("WM_DELETE_WINDOW", lambda : self.repoe_botoes_final(janela_info))
        if idioma == "PT":
            janela_info.title("Informação sobre a personalidade")
        else:
            janela_info.title("Information about personalities")
        janela_info.resizable(False, False)
        self.janela_init.eval(f'tk::PlaceWindow {str(janela_info)} center')
        
        fr1 = tk.Frame(janela_info)
        fr2 = tk.Frame(janela_info)
        tit = tk.Label(fr1, text=tit_personalidade, justify="center", font=("Arial", 25, "bold" ))
        tit.pack()
        texto = tk.Label(fr2, text=inf_personalidade, justify="center")
        texto.pack()

        imagem_rep_tk = tk.PhotoImage(file=img_path)
        imagem_reduzida = imagem_rep_tk.subsample(2, 2)

        fr3 = tk.Label(janela_info, image=imagem_reduzida)
        fr3.image = imagem_reduzida

        fr1.pack()
        fr2.pack()
        fr3.pack()

    # cria e verifica se o ficheiro já existe
    # retona False se o ficheiro já existir
    # rtorna True se o ficheiro foi criado
    def cria_ficheiro(self) -> bool:
        if os.path.exists("email-cache.bin"):
            return False
        else:
            ficheiro = open("email-cache.bin", "wb") # apenas cria ficheiro
            ficheiro.close()
            return True

    def le_cache(self, email_str) -> bool:
        encontrou = False
        email_cache_leitura = open("email-cache.bin", "rb")
        for string in email_cache_leitura:
            if email_str == string.decode("utf-8"):
                encontrou = True # encontrou email na cache local do computador
                break
        email_cache_leitura.close()
        return encontrou

    def ver_registro(self):
        winsound.PlaySound(diretorio_audio_b, fich_async)
        global idioma
        if not os.path.exists("resultado.xml"):
            if idioma == "PT":
                tk.messagebox.showinfo("Sem dados", "Não foi detectado nenhum dado no registro, realize um teste")
            else:
                tk.messagebox.showinfo("Data empty", "No data was detected in the log, perform a test")
            return 1

        self.janela_reg = Toplevel(self.janela_init)
        if idioma == "PT":
            self.janela_reg.title("Registro")
        else:
            self.janela_reg.title("Register")
        self.janela_init.eval(f'tk::PlaceWindow {str(self.janela_reg)} center')

        self.botao_init["state"] = "disabled"
        self.botao_registo["state"] = "disabled"
        self.botao_idioma["state"] = "disabled"
        self.botao_rank["state"] = "disabled"

        self.janela_reg.protocol("WM_DELETE_WINDOW", self.repoe_botoes_init_reg)

        colunas = ('Nome', 'Email', 'Resultado', 'Data')

        grelha = ttk.Treeview(self.janela_reg, columns=colunas, show='headings')

        rolagem = Scrollbar(self.janela_reg, orient="vertical", command=grelha.yview)
        rolagem.pack(side="right", fill="y")

        grelha.config(yscrollcommand=rolagem.set)

        grelha.heading('Email', text='Email')
        grelha.heading('Data', text='Data')
        if idioma == "PT":
            grelha.heading('Nome', text='Nome')
            grelha.heading('Resultado', text='Resultado')
        else:
            grelha.heading('Nome', text='Name')
            grelha.heading('Resultado', text='Result')

        dados_formatados = self.le_registro_xml()

        num_dados = len(dados_formatados) - 1

        for linha in range(num_dados,0,-1):
            grelha.insert("", tk.END, values=(dados_formatados[linha][0], dados_formatados[linha][1], self.tipos.resultado_str[int(dados_formatados[linha][2])], dados_formatados[linha][3]))

        grelha.pack(expand=True, fill=tk.BOTH)
        
    def repoe_botoes_init_reg(self) -> None:
        self.botao_init["state"] = "normal"
        self.botao_registo["state"] = "normal"
        self.botao_idioma["state"] = "normal"
        self.botao_rank["state"] = "normal"
        self.janela_reg.destroy()

    def repoe_botoes_final(self, janela_inf) -> None:
        self.botao_info["state"] = "normal"
        self.botao_menu["state"] = "normal"
        janela_inf.destroy()

    def repoe_botoes_init_idioma(self) -> None:
        self.botao_init["state"] = "normal"
        self.botao_registo["state"] = "normal"
        self.botao_idioma["state"] = "normal"
        self.botao_rank["state"] = "normal"
        self.janela_def.destroy()

    def repoe_botoes_init_rank(self) -> None:
        self.botao_init["state"] = "normal"
        self.botao_registo["state"] = "normal"
        self.botao_idioma["state"] = "normal"
        self.botao_rank["state"] = "normal"
        self.janela_rank.destroy()

    def verificar_mudou_idioma(self, idioma_e) -> None:
        self.tipos.verificar_idioma(idioma_e)
        global mudou
        if mudou == True:
            self.imagem.close()
            self.imagem_botao.close()
            self.imagem_reg.close()
            self.imagem_botao_idioma.close()
            self.imagem = Image.open(self.tipos.caminho_img_fundo_init_str)
            self.imagem.thumbnail((1920, 1080))
            self.imagem_tk = ImageTk.PhotoImage(self.imagem)
            self.label1.configure(image=self.imagem_tk)
            self.label1.image = self.imagem_tk
            self.imagem_botao = Image.open(self.tipos.caminho_img_botoes_str[0])
            self.imagem_botao_f = ImageTk.PhotoImage(self.imagem_botao)
            self.botao_init.configure(image=self.imagem_botao_f)
            self.botao_init.image = self.imagem_botao_f
            self.imagem_reg = Image.open(self.tipos.caminho_img_botoes_str[1])
            self.imagem_reg_f = ImageTk.PhotoImage(self.imagem_reg)
            self.botao_registo.configure(image=self.imagem_reg_f)
            self.botao_registo.image = self.imagem_reg_f
            self.imagem_botao_idioma = Image.open(self.tipos.caminho_img_botoes_str[2])
            self.imagem_botao_idioma_f = ImageTk.PhotoImage(self.imagem_botao_idioma)
            self.botao_idioma.configure(image=self.imagem_botao_idioma_f)
            self.botao_idioma.image = self.imagem_botao_idioma_f
            self.rotulo_nome["text"] = self.tipos.nome_text
            self.repoe_botoes_init_idioma()

    def idioma_janela(self) -> None:
        self.janela_def = Toplevel(self.janela_init)
        self.janela_def.resizable(False, False)
        if idioma == "PT":
            self.janela_def.title("Idioma")
        else:
            self.janela_def.title("Language")
        self.janela_init.eval(f'tk::PlaceWindow {str(self.janela_def)} center')
        self.botao_init["state"] = "disabled"
        self.botao_registo["state"] = "disabled"
        self.botao_idioma["state"] = "disabled"
        self.botao_rank["state"] = "disabled"

        self.janela_def.protocol("WM_DELETE_WINDOW", self.repoe_botoes_init_idioma)

        idioma_b = tk.StringVar(value=idioma)
        if idioma == "PT":
            self.idiomas = tk.LabelFrame(self.janela_def, text="idiomas")
            botao_r_in = ttk.Radiobutton(self.idiomas, text='Inglês', value='IN', variable=idioma_b)
            botao_r_pt = ttk.Radiobutton(self.idiomas, text='Português', value='PT', variable=idioma_b)
            botao_aplicar_idioma = tk.Button(self.idiomas, text="Aplicar idioma", command=lambda: self.verificar_mudou_idioma(idioma_b))
        else:
            self.idiomas = tk.LabelFrame(self.janela_def, text="languages")
            botao_r_in = ttk.Radiobutton(self.idiomas, text='English', value='IN', variable=idioma_b)
            botao_r_pt = ttk.Radiobutton(self.idiomas, text='Portuguese', value='PT', variable=idioma_b)
            botao_aplicar_idioma = tk.Button(self.idiomas, text="Aply Language", command=lambda: self.verificar_mudou_idioma(idioma_b))
        botao_r_in.grid(row=0, column=0, padx=5, pady=5)  # Primeiro botão
        botao_r_pt.grid(row=0, column=1, padx=5, pady=5)  # Segundo botão ao lado do primeiro
        botao_aplicar_idioma.grid(row=1, columnspan=2, pady=5)  # Terceiro botão abaixo dos dois primeiros
        self.idiomas.pack(fill="both", expand=True)

    def rank(self) -> None:
        winsound.PlaySound(diretorio_audio_b, fich_async)
        try:
            dados_resultados = receber_dados()
        except:
            if idioma == "PT":
                tk.messagebox.showinfo("Erro de rede", "Não foi possivel estabelecer ligação ao banco de dados")
            else:
                tk.messagebox.showinfo("Network error", "Unable to connect to database")
            return 1

        self.janela_rank = Toplevel(self.janela_init)
        self.janela_rank.title("Ranking")
        self.janela_init.eval(f'tk::PlaceWindow {str(self.janela_rank)} center')
        self.janela_rank.resizable(False, False)

        self.botao_init["state"] = "disabled"
        self.botao_registo["state"] = "disabled"
        self.botao_idioma["state"] = "disabled"
        self.botao_rank["state"] = "disabled"

        self.janela_rank.protocol("WM_DELETE_WINDOW", self.repoe_botoes_init_rank)

        quantidade_tipos = list(range(9))
        quantidade_tipos_str = ['' for _ in range(9)]
        quantidade_tipos_str_int = list(range(9))

        for i in range(9):
            quantidade_tipos_str[i] = str(dados_resultados).count(str(i+1))
            quantidade_tipos[i] = int(quantidade_tipos_str[i])
            quantidade_tipos_str_int[i] = i + 1

        total_dados = sum(quantidade_tipos)

        # ordena
        linha = 0
        while linha < 9:
            coluna = linha + 1
            while coluna < 9:
                if quantidade_tipos[linha] < quantidade_tipos[coluna]:
                    tmp = quantidade_tipos[linha]
                    quantidade_tipos[linha] = quantidade_tipos[coluna]
                    quantidade_tipos[coluna] = tmp
                    tmp = quantidade_tipos_str_int[linha]
                    quantidade_tipos_str_int[linha] = quantidade_tipos_str_int[coluna]
                    quantidade_tipos_str_int[coluna] = tmp
                    linha = 0
                else:
                    coluna += 1
            linha += 1

        colunas = ('Lugar', 'Tipo', 'Quantidade_bruta', 'Percentagem')

        grelha = ttk.Treeview(self.janela_rank, columns=colunas, show='headings')

        if idioma == "PT":
            grelha.heading('Lugar', text='Classificação')
            grelha.heading('Tipo', text='Tipo')
            grelha.heading('Quantidade_bruta', text='Total')
            grelha.heading('Percentagem', text='Total porcento (%)')
        else:
            grelha.heading('Lugar', text='Classification')
            grelha.heading('Tipo', text='Type')
            grelha.heading('Quantidade_bruta', text='Total')
            grelha.heading('Percentagem', text='Total porcentage (%)')

        for coluna in colunas:
            grelha.column(coluna, anchor='center')

        if idioma == "PT":
            lugar = "º Lugar"
        else:
            lugar = " Place"

        for num in range(9):
            grelha.insert("", tk.END, values=(str(num+1) + lugar, self.tipos.resultado_str[quantidade_tipos_str_int[num]], quantidade_tipos[num], str(round((quantidade_tipos[num] / total_dados) * 100, 1)) + "%")) # porentagem fica para a frente
        
        grelha.pack(expand=True, fill=tk.BOTH)

    # atributos globais
    resultado_do_user = 0
    interrupted_rede = False

    def verifica_rede(self, mutex_rede) -> bool:
        global interrupted_rede
        while not interrupted_rede:
            mutex_rede.acquire()
            try:
                _ = requests.get("http://www.google.com", timeout=10)
                self.rede = True
            except:
                self.rede = False
            finally:
           #     if self.mutex.locked():
                mutex_rede.release()
            time.sleep(0.1)
        return 0

    def voltar(self) -> bool:
        pergunta = ""
        global idioma
        if idioma == "PT":
            pergunta = tk.messagebox.askquestion("Sair do teste", "Tem a certeza que quer sair do teste?", detail="Os dados serão perdidos.")
        else:
            pergunta = tk.messagebox.askquestion("Quit test", "Are you sure you want to get out of the test?", detail="The data will be lost.")
        if pergunta == "no":
            return 0
        else:
            for widget in self.janela_init.winfo_children():
                widget.destroy()
            self.__init__(self.janela_init, self.tipos)

    def __init__ (self, janela_init, tipos) -> None:
        self.janela_init = janela_init
        self.tipos = tipos
        self.janela_init.title("Teste de personalidade")
        self.janela_init.geometry("1920x1080")
        self.imagem = Image.open(self.tipos.caminho_img_fundo_init_str)
        self.imagem.thumbnail((1920, 1080))
        self.imagem_tk = ImageTk.PhotoImage(self.imagem)

        self.label1 = Label(self.janela_init, image=self.imagem_tk)
        self.label1.pack()

        self.label1.imagem = self.imagem_tk

        imagem_logo = Image.open(diretorio_g + "logo.png")
        logo = ImageTk.PhotoImage(imagem_logo)

        self.imagem_botao = Image.open(self.tipos.caminho_img_botoes_str[0])
        self.imagem_botao_f = ImageTk.PhotoImage(self.imagem_botao)

        self.imagem_reg = Image.open(self.tipos.caminho_img_botoes_str[1])
        self.imagem_reg_f = ImageTk.PhotoImage(self.imagem_reg)

        self.imagem_botao_idioma = Image.open(self.tipos.caminho_img_botoes_str[2])
        self.imagem_botao_idioma_f = ImageTk.PhotoImage(self.imagem_botao_idioma)

        self.imagem_botao_rank = Image.open(diretorio_g + "rank.png")
        self.imagem_botao_rank_f = ImageTk.PhotoImage(self.imagem_botao_rank)

        # Defina a imagem como ícone
        self.janela_init.iconphoto(True, logo)
        self.mensagem_principal = tk.Label()
        self.email_entry = tk.Entry(width=40, exportselection=True)
        self.nome = tk.Entry(width=40, exportselection=True)
        self.rotulo_nome = tk.Label(text=self.tipos.nome_text, font=("Arial", 15, "bold"), bg="pink")
        self.rotulo_email = tk.Label(text="Email:", font=("Arial", 15, "bold"), bg="pink")
        self.botao_registo = tk.Button(janela_init, image=self.imagem_reg_f, width=180, height=30, command=self.ver_registro)
        self.botao_init = tk.Button(janela_init, image=self.imagem_botao_f, width=250, height=50, command=self.verifica)
        self.botao_idioma = tk.Button(janela_init, image=self.imagem_botao_idioma_f, width=180, height=30, text="Idioma", command=self.idioma_janela)
        self.botao_rank = tk.Button(janela_init, image=self.imagem_botao_rank_f, width=180, height=30, command=self.rank)
        self.botao_init.image = self.imagem_botao_f
        self.botao_registo.image = self.imagem_reg_f
        self.botao_idioma.image = self.imagem_botao_idioma_f
        self.rotulo_nome.place(x=540, y=240)
        self.rotulo_email.place(x=540, y=290)
        self.botao_idioma.place(x=570, y=470)
        self.nome.place(x=540, y=270)
        self.email_entry.place(x=540, y=320)
        self.botao_init.place(x=540, y=360)
        self.botao_registo.place(x=570, y=430)
        self.botao_rank.place(x=570, y=510)

    def verifica(self) -> bool:
        winsound.PlaySound(diretorio_audio_b, fich_async)
        global idioma
        self.idioma = idioma
        global interrupted_rede
        interrupted_rede = False
        self.nome_id = self.nome.get()
        self.rede = True
        self.email_check = self.email_entry.get()
        self.pergunta = ""
        econtrou = False
        mutex = threading.Lock()
        if self.nome_id == "":
            if self.idioma == "PT":
                tk.messagebox.showerror("Preencha o campo nome", "É obrigatorio introduzor o nome")
            else:
                tk.messagebox.showerror("Fill in the name field", "It is mandatory to enter the name")
            self.nome.config(bg="#FFC0CB")
            return 1
        elif self.email_check == "":
            if self.idioma == "PT":
                tk.messagebox.showerror("Preencha o campo email", "É obrigatorio introduzor o email")
            else:
                tk.messagebox.showerror("Fill in the email field", "It is mandatory to enter the email")
            self.email_entry.config(bg="#FFC0CB")
            return 1
        elif self.email_check == "":
            if self.idioma == "PT":
                tk.messagebox.showerror("Preencha o campo email", "É obrigatorio introduzor o email")
            else:
                tk.messagebox.showerror("Fill in the email field", "It is mandatory to enter the email")
            self.email_entry.config(bg="#FFC0CB")
            return 1
        elif self.cria_ficheiro() == False:
            econtrou = self.le_cache(self.email_check + "\n")

        tarefa_rede = threading.Thread(target=self.verifica_rede, args=(mutex, ), daemon=True)
        tarefa_rede.start()

        mutex.acquire()
        # sem o acesso á rede não podemos validar o email
        if econtrou == False and self.rede == True:
            mutex.release()
            if not validate_email(email_address=self.email_check):
                mutex.acquire()
                if self.rede == True:
                    if self.idioma == "PT":
                        tk.messagebox.showerror("Email invalido", "O email introduzido é invlido ou não existe, reescreva")
                    else:
                        tk.messagebox.showerror("Invalid Email", "The email you entered does not exist, please rewrite")
                    self.email_entry.config(bg="#FFC0CB")
                    interrupted_rede = True
                    mutex.release()
                    return 1
                else:
                    if self.idioma == "PT":
                        self.pergunta = tk.messagebox.askquestion("Erro de rede", "Não foi possível estabelecer conexão á rede, deseja continuar com o teste?")
                    else:
                        self.pergunta = tk.messagebox.askquestion("Network error", "Unable to connect to the network, do you want to continue with the test?")
                    mutex.release()
            else: # se o email estiver correto mas o utilizador não tiver o acessso a rede o email não sera guardado no ficheiro de cache
                ficheiro_cache_escrita = open("email-cache.bin", "ab")
                ficheiro_cache_escrita.write((self.email_check + "\n").encode('utf-8'))
                ficheiro_cache_escrita.close()
        elif self.rede == False:
            if self.idioma == "PT":
                self.pergunta = tk.messagebox.askquestion("Erro de rede", "Não foi possível estabelecer conexão á rede, deseja continuar com o teste?")
            else:
                self.pergunta = tk.messagebox.askquestion("Network error", "Unable to connect to the network, do you want to continue with the test?")

        if mutex.locked():
            mutex.release()
        interrupted_rede = True

        if self.pergunta == "no":
            return 1

        self.botao_init.destroy()
        self.nome.destroy()
        self.rotulo_nome.destroy()
        self.rotulo_email.destroy()
        self.botao_registo.destroy()
        self.email_entry.destroy()
        self.imagem.close()
        self.imagem_botao_idioma.close()
        self.imagem_reg.close()
        self.imagem_botao_rank.close()
        self.botao_idioma.destroy()
        self.botao_rank.destroy()
        self.init_cinzento()

    def init_cinzento(self) -> None:
        self.imagem = Image.open(diretorio_g + "cinzento.jpg")
        self.imagem.thumbnail((1920, 1080))
        self.imagem_tk = ImageTk.PhotoImage(self.imagem)
        self.label1.configure(image=self.imagem_tk)
        self.label1.image = self.imagem_tk
        if idioma == "PT":
            self.botao_sair = Button(self.janela_init, text="Sair do teste", command=self.voltar, background="red")
        else:
            self.botao_sair = Button(self.janela_init, text="Quit test", command=self.voltar, background="red")
        self.botao_sair.place(x=20, y=15)
        if self.idioma == "PT":
            self.mensagem_principal.config(text="Escolha uma das opções", bg="#808080", font=("Arial", 25, "bold"), justify="center")
        else:
            self.mensagem_principal.config(text="Choose one option", bg="#808080", font=("Arial", 25, "bold"), justify="center")
        self.imagem_botao_pergunta = Image.open(diretorio_g + "botao_c.png")
        self.imagem_botao_pergunta_tk = ImageTk.PhotoImage(self.imagem_botao_pergunta)
        self.Botao1 = tk.Button(self.janela_init, background="#ccc8c0", text=self.tipos.tipo_cinzento_str[8], width=80, height=2, command=lambda: self.cinzento2(8))
        self.Botao2 = tk.Button(self.janela_init, background="#ccc8c0", text=self.tipos.tipo_cinzento_str[5], width=80, height=2, command=lambda: self.cinzento2(5))
        self.Botao3 = tk.Button(self.janela_init, background="#ccc8c0", text=self.tipos.tipo_cinzento_str[2], width=80, height=2, command=lambda: self.cinzento2(2))
        self.Botao1.place(x=50, y=450)
        self.Botao2.place(x=350, y=300)
        self.Botao3.place(x=650, y=450)
        if self.idioma == "PT":
            self.mensagem_principal.place(x=450, y=150)
        else:
            self.mensagem_principal.place(x=500, y=150)

    def cinzento2(self, resp_num) -> None:
        winsound.PlaySound(diretorio_audio_b, fich_async)
        self.tipos.resp[0] = resp_num
        self.Botao1.config(command=lambda: self.cinzento3(6), text=self.tipos.tipo_cinzento_str[6])
        self.Botao2.config(command=lambda: self.cinzento3(7), text=self.tipos.tipo_cinzento_str[7])
        self.Botao3.config(command=lambda: self.cinzento3(1), text=self.tipos.tipo_cinzento_str[1])

    def cinzento3(self, resp_num) -> None:
        winsound.PlaySound(diretorio_audio_b, fich_async)
        self.tipos.resp[1] = resp_num
        self.Botao1.config(command=lambda: self.cinzento4(3), text=self.tipos.tipo_cinzento_str[3])
        self.Botao2.config(command=lambda: self.cinzento4(4), text=self.tipos.tipo_cinzento_str[4])
        self.Botao3.config(command=lambda: self.cinzento4(9), text=self.tipos.tipo_cinzento_str[9])

    def cinzento4(self, resp_num) -> None:
        winsound.PlaySound(diretorio_audio_b, fich_async)
        self.tipos.resp[2] = resp_num
        self.Botao1.config(command=lambda: self.cinzento5(7), text=self.tipos.tipo_cinzento_str[7])
        self.Botao2.config(command=lambda: self.cinzento5(3), text=self.tipos.tipo_cinzento_str[3])
        self.Botao3.config(command=lambda: self.cinzento5(9), text=self.tipos.tipo_cinzento_str[9])

    def cinzento5(self, resp_num) -> None:
        winsound.PlaySound(diretorio_audio_b, fich_async)
        self.tipos.resp[3] = resp_num
        self.Botao1.config(command=lambda: self.cinzento6(4), text=self.tipos.tipo_cinzento_str[4])
        self.Botao2.config(command=lambda: self.cinzento6(1), text=self.tipos.tipo_cinzento_str[1])
        self.Botao3.config(command=lambda: self.cinzento6(8), text=self.tipos.tipo_cinzento_str[8])

    def cinzento6(self, resp_num) -> None:
        winsound.PlaySound(diretorio_audio_b, fich_async)
        self.tipos.resp[4] = resp_num
        self.Botao1.config(command=lambda: self.cinzento7(5), text=self.tipos.tipo_cinzento_str[5])
        self.Botao2.config(command=lambda: self.cinzento7(2), text=self.tipos.tipo_cinzento_str[2])
        self.Botao3.config(command=lambda: self.cinzento7(6), text=self.tipos.tipo_cinzento_str[6])

    def cinzento7(self, resp_num) -> None:
        winsound.PlaySound(diretorio_audio_b, fich_async)
        self.tipos.resp[5] = resp_num
        self.Botao1.config(command=lambda: self.cinzento8(7), text=self.tipos.tipo_cinzento_str[7])
        self.Botao2.config(command=lambda: self.cinzento8(9), text=self.tipos.tipo_cinzento_str[9])
        self.Botao3.config(command=lambda: self.cinzento8(2), text=self.tipos.tipo_cinzento_str[2])
    
    def cinzento8(self, resp_num) -> None:
        winsound.PlaySound(diretorio_audio_b, fich_async)
        self.tipos.resp[6] = resp_num
        self.Botao1.config(command=lambda: self.cinzento9(6), text=self.tipos.tipo_cinzento_str[6])
        self.Botao2.config(command=lambda: self.cinzento9(8), text=self.tipos.tipo_cinzento_str[8])
        self.Botao3.config(command=lambda: self.cinzento9(4), text=self.tipos.tipo_cinzento_str[4])
    
    def cinzento9(self, resp_num) -> None:
        winsound.PlaySound(diretorio_audio_b, fich_async)
        self.tipos.resp[7] = resp_num
        self.Botao1.config(command=lambda: self.cinzento10(5), text=self.tipos.tipo_cinzento_str[5])
        self.Botao2.config(command=lambda: self.cinzento10(1), text=self.tipos.tipo_cinzento_str[1])
        self.Botao3.config(command=lambda: self.cinzento10(3), text=self.tipos.tipo_cinzento_str[3])
    
    def cinzento10(self, resp_num) -> None:
        winsound.PlaySound(diretorio_audio_b, fich_async)
        self.tipos.resp[8] = resp_num
        self.Botao1.config(command=lambda: self.cinzento11(9), text=self.tipos.tipo_cinzento_str[9])
        self.Botao2.config(command=lambda: self.cinzento11(8), text=self.tipos.tipo_cinzento_str[8])
        self.Botao3.config(command=lambda: self.cinzento11(3), text=self.tipos.tipo_cinzento_str[3])
    
    def cinzento11(self, resp_num) -> None:
        winsound.PlaySound(diretorio_audio_b, fich_async)
        self.tipos.resp[9] = resp_num
        self.Botao1.config(command=lambda: self.cinzento12(4), text=self.tipos.tipo_cinzento_str[4])
        self.Botao2.config(command=lambda: self.cinzento12(7), text=self.tipos.tipo_cinzento_str[7])
        self.Botao3.config(command=lambda: self.cinzento12(1), text=self.tipos.tipo_cinzento_str[1])
    
    def cinzento12(self, resp_num) -> None:
        winsound.PlaySound(diretorio_audio_b, fich_async)
        self.tipos.resp[10] = resp_num
        self.Botao1.config(command=lambda: self.init_fase_rosa(2), text=self.tipos.tipo_cinzento_str[2])
        self.Botao2.config(command=lambda: self.init_fase_rosa(6), text=self.tipos.tipo_cinzento_str[6])
        self.Botao3.config(command=lambda: self.init_fase_rosa(5), text=self.tipos.tipo_cinzento_str[5])
    
    def init_fase_rosa(self, resp_num) -> None:
        winsound.PlaySound(diretorio_audio_b, fich_async)
        self.imagem.close()
        self.imagem = Image.open(diretorio_g + "rosa.jpg")
        self.imagem.thumbnail((1920, 1080))
        self.imagem_tk = ImageTk.PhotoImage(self.imagem)
        self.label1.configure(image=self.imagem_tk)
        self.label1.image = self.imagem_tk
        self.mensagem_principal["bg"] = "pink"
        self.tipos.resp[11] = resp_num
        self.Botao1.config(command=lambda: self.rosa_2(self.tipos.resp[0], 0, 3), background="#edcedf", text=self.tipos.tipo_rosa_str[self.tipos.resp[0]])
        self.Botao2.config(command=lambda: self.rosa_2(self.tipos.resp[1], 0, 3), background="#edcedf", text=self.tipos.tipo_rosa_str[self.tipos.resp[1]])
        self.Botao3.config(command=lambda: self.rosa_2(self.tipos.resp[2], 0, 3), background="#edcedf", text=self.tipos.tipo_rosa_str[self.tipos.resp[2]])

    def rosa_2(self, resp_num, index_resp, index_text) -> None:
        winsound.PlaySound(diretorio_audio_b, fich_async)
        self.tipos.fase_2_resp[index_resp] = resp_num
        if index_text == 12:
            self.verifica_repeticao() # parametro apenas de trensporte
        else:
            self.Botao1.config(command=lambda: self.rosa_2(self.tipos.resp[index_text], index_resp+1, index_text+3), text=self.tipos.tipo_rosa_str[self.tipos.resp[index_text]])
            self.Botao2.config(command=lambda: self.rosa_2(self.tipos.resp[index_text+1], index_resp+1, index_text+3), text=self.tipos.tipo_rosa_str[self.tipos.resp[index_text+1]])
            self.Botao3.config(command=lambda: self.rosa_2(self.tipos.resp[index_text+2], index_resp+1, index_text+3), text=self.tipos.tipo_rosa_str[self.tipos.resp[index_text+2]])

    def verifica_repeticao(self) -> None:
        winsound.PlaySound(diretorio_audio_b, fich_async)
        i = 0
        while i < 3:
            j = i + 1
            while j < 4:
                if self.tipos.fase_2_resp[i] == self.tipos.fase_2_resp[j]:
                    self.tipos.fase_2_resp[j] = random.choice(self.tipos.resp)
                    i = 0
                else:
                    j += 1
            i += 1  
        self.fase_rosa2_1()

    def fase_rosa2_1(self) -> None:
        winsound.PlaySound(diretorio_audio_b, fich_async)
        self.Botao1.config(command=lambda: self.fase_rosa2_2(self.tipos.fase_2_resp[0]), background="#cde2fc", text=self.tipos.tipo_rosa_str[self.tipos.fase_2_resp[0]])
        self.Botao2.config(command=lambda: self.fase_rosa2_2(self.tipos.fase_2_resp[1]), background="#cde2fc", text=self.tipos.tipo_rosa_str[self.tipos.fase_2_resp[1]])
        self.Botao3.config(command=lambda: self.fase_rosa2_2(self.tipos.fase_2_resp[2]), background="#cde2fc", text=self.tipos.tipo_rosa_str[self.tipos.fase_2_resp[2]])
        
    def fase_rosa2_2(self, resp_num) -> None:
        winsound.PlaySound(diretorio_audio_b, fich_async)
        self.tipos.fase_2_1_resp[0] = resp_num
        self.Botao1.config(command=lambda: self.leve_verificação(self.tipos.fase_2_resp[1]), text=self.tipos.tipo_rosa_str[self.tipos.fase_2_resp[1]])
        self.Botao2.config(command=lambda: self.leve_verificação(self.tipos.fase_2_resp[2]), text=self.tipos.tipo_rosa_str[self.tipos.fase_2_resp[2]])
        self.Botao3.config(command=lambda: self.leve_verificação(self.tipos.fase_2_resp[3]), text=self.tipos.tipo_rosa_str[self.tipos.fase_2_resp[3]])

    def leve_verificação(self, resp_num) -> None:
        winsound.PlaySound(diretorio_audio_b, fich_async)
        self.tipos.fase_2_1_resp[1] = resp_num
        contador = 2
        while 1:
            if self.tipos.fase_2_1_resp[0] == self.tipos.fase_2_1_resp[1]:
                self.tipos.fase_2_1_resp[1] = self.tipos.fase_2_resp[contador] # solução para um pequeno bug
                contador += 1
            else:
                break
        self.init_azul()

    def init_azul(self) -> None:
        self.imagem.close()
        self.imagem = Image.open(diretorio_g + "azul.jpg")
        self.imagem.thumbnail((1920, 1080))
        self.imagem_tk = ImageTk.PhotoImage(self.imagem)
        self.label1.configure(image=self.imagem_tk)
        self.label1.image = self.imagem_tk
        self.mensagem_principal["bg"] = "blue"
        self.Botao2.destroy()
        self.Botao1.config(command=lambda: self.resultado_final(self.tipos.fase_2_1_resp[0]), text=self.tipos.tipo_azul_str[self.tipos.fase_2_resp[0]])
        self.Botao3.config(command=lambda: self.resultado_final(self.tipos.fase_2_1_resp[1]), text=self.tipos.tipo_azul_str[self.tipos.fase_2_resp[1]])

    def resultado_final(self, resp_num) -> None:
        winsound.PlaySound(diretorio_audio_b, fich_async)
        tempo = strftime("%d/%m/%Y %H:%M:%S", gmtime(time.time()))
        self.imagem_botao_pergunta.close()
        self.mensagem_principal.destroy()
        self.imagem = Image.open(diretorio_g + "resultado.png")
        imagem_tk = ImageTk.PhotoImage(self.imagem)
        self.img_menu = Image.open(self.tipos.caminho_img_botoes_str[3])
        img_menu_tk = ImageTk.PhotoImage(self.img_menu)
        self.img_inf = Image.open(self.tipos.caminho_img_botoes_str[4])
        img_inf_tk = ImageTk.PhotoImage(self.img_inf)
        self.label1.configure(image=imagem_tk)

        self.label1.imagem = imagem_tk
        self.Botao3.destroy()
        self.Botao1.destroy()
        self.botao_sair.destroy()

        self.resultado_do_user = self.tipos.resultado_str[resp_num]
        if self.idioma == "PT":
            self.Resultado = tk.Label(bg="purple", font=("Arial", 30, "bold"), text="O seu tipo é " + str(resp_num) + "-" + self.tipos.resultado_str[resp_num])
        else:
            self.Resultado = tk.Label(bg="purple", font=("Arial", 30, "bold"), text="Your type is " + str(resp_num) + "-" + self.tipos.resultado_str[resp_num])
        self.botao_menu = tk.Button(width=200, height=40, image=img_menu_tk, command=self.fim)
        self.botao_info = tk.Button(width=200, height=60, image=img_inf_tk, command=lambda: self.mostrar_info(self.tipos.inf_personalidade_str[resp_num], self.resultado_do_user, diretorio_g + self.tipos.caminho_img_fundo_str[resp_num]))
        self.botao_menu.image = img_menu_tk
        self.botao_info.image = img_inf_tk
        self.botao_menu.place(x=540, y=350)
        self.botao_info.place(x=540, y=410)
        if self.idioma == "PT":
            self.Resultado.place(x=430,y=150)
        else:
            self.Resultado.place(x=380, y=150)
        fich_xml = self.cria_xml()
        num_resultados = len(list(self.dados))
        resultado_lista = {"nome": self.nome_id, "email": self.email_check, "resultado": resp_num, "tempo": tempo}
        self.escreve_resultado_xml(self.dados, "teste" + str(num_resultados), resultado_lista)
        fich_xml.write("resultado.xml")
        if self.pergunta == "": # não ocorreu erro de rede na primeira fase
            while 1:
                try:
                    enviar_email(self.nome_id, self.email_check, self.tipos.resultado_str[resp_num], tempo, self.tipos.inf_personalidade_str[resp_num])
                    inserir_usuario(self.nome_id, self.email_check, resp_num, tempo)
                    break
                except:
                    if idioma == "PT":
                        resposta = tk.messagebox.askquestion("Erro de conexão", "Não foi possivel conectar ao banco de dados, deseja tentar outra vez?", icon='error')
                    else:
                        resposta = tk.messagebox.askquestion("Connection error", "Unable to connect database, try again?", icon='error')
                    if resposta == "no":
                        break

    def fim(self) -> None:
        winsound.PlaySound(diretorio_audio_b, fich_async)
        self.botao_menu.destroy()
        self.botao_info.destroy()
        self.imagem.close()
        self.img_inf.close()
        self.img_menu.close()
        self.label1.destroy()
        self.Resultado.destroy()
        self.__init__(self.janela_init, self.tipos)

# Inicio do programa
# inicia o diretorio dos assets
dir = os.path.dirname(os.path.abspath(sys.argv[0]))
diretorio_g = dir + "\\assets" + "\\img\\"
diretorio_audio = dir + "\\assets" + "\\sound\\"
diretorio_audio_b = diretorio_audio + "zapsplat_multimedia_button_click_bright_003_92100.wav"
inicializa_diretorio()
# detecta o idioma
personalidades = tipos_personalidade()
detectar_idioma_padrao()
personalidades.mudar_idioma(idioma)
#inicia a janela
janela = Tk()
if not os.path.exists(dir + "\\assets"):
    janela.withdraw()
    if idioma == "PT":
        tk.messagebox.showerror("Arquivo não encontrado", "Não foi possivel encontrar o arquivo assets do programa.")
    else:
        tk.messagebox.showerror("Resources not found", "Unable to find the program assets file.")
    sys.exit(1)
app = App(janela, personalidades)
janela.mainloop()
