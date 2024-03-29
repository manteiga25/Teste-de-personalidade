from tkinter import *
import tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from functools import partial
import winsound
import random
from validate_email import validate_email
import os
import sys
from PIL import Image, ImageTk
import requests
import threading
import xml.etree.ElementTree as ET
import time
from time import gmtime, strftime

#Variavel Global do programa todo
audio_async = winsound.SND_FILENAME | winsound.SND_ASYNC
rede_quest = True

class tipos_personalidade:
    
    # lista com as respostas
    resp = list(range(12))
    fase_2_resp = list(range(4))
    
    # variaveis fase rosa
    tipo_rosa_str = ['' for _ in range(10)]
    
    tipo_rosa_str[0] = ""
    tipo_rosa_str[1] = "Os outros veem-me como perfeccionista, Disciplina e rigor são importantes para mim"
    tipo_rosa_str[2] = "Os outros veem-me como disponível, Conexão com os outros e ajudar é importante para mim"
    tipo_rosa_str[3] = "Os outros veem-me como alguém bem sucedido, O resultado e o reconhecimento são importantes para mim"
    tipo_rosa_str[4] = "Os outros veem-me como alguém diferente, Sentir-me especial é importante para mim"
    tipo_rosa_str[5] = "Os outros veem-me como alguém frio e distante, Conhecimento e isolamento são importantes para mim"
    tipo_rosa_str[6] = "Os outros veem-me como alguém desconfiado, Antecipação de cenários é importantepara mim"
    tipo_rosa_str[7] = "Os outros veem-me como alguém entusiasta, Ter planos e várias opções é importante para mim"
    tipo_rosa_str[8] = "Os outros veem-me como alguém demasiado frontal, Controlo é importante para mim"
    tipo_rosa_str[9] = "Os outros veem-me como alguém flexível, Harmonia éimportante para mim"

    # variaveis fase azul
    tipo_azul_str = ['' for _ in range(10)]

    tipo_azul_str[0] = ""
    tipo_azul_str[1] = "Foco no acerto e errado, Alto nível de exigência, Foco no detalhe e no rigor"
    tipo_azul_str[2] = "Foco em ajudar os outros,  Fácil comunicar e relacionar, Proatividade na ajuda aos outros"
    tipo_azul_str[3] = "Foco nas metas e concretização, Vaidade pelas suas conquistas, Foco na imagem e performance"
    tipo_azul_str[4] = "Preocupação em ser diferente, Intensidade emocional, Muito exigenteconsigo mesmo"
    tipo_azul_str[5] = "Foco na sua privacidade, Prazer pelo isolamento, Frieza, lógica e racionalidade"
    tipo_azul_str[6] = "Foco em antecipar, Dificuldade em confiar, Hábil em fazer questões"
    tipo_azul_str[7] = "Foco em manter varias opções, Entusiasmo e criatividade, Otimismo e foco no prazer"
    tipo_azul_str[8] = "Foco em manter o controlo, Frontalidade e assertividade, Justiça e defesa dos mais fracos"
    tipo_azul_str[9] = "Foco na harmonia e consenso, Dificuldade em dizer não, Flexibilidade em aceitar os outros"

    # resultado
    resultado_str = ['' for _ in range(10)]

    resultado_str[0] = ""
    resultado_str[1] = "Perfecionista"
    resultado_str[2] = "Prestativo"
    resultado_str[3] = "Bem-sucedido"
    resultado_str[4] = "Romantico"
    resultado_str[5] = "Frio"
    resultado_str[6] = "Questionador"
    resultado_str[7] = "Sonhador"
    resultado_str[8] = "Confrontador"
    resultado_str[9] = "Controlador"

    inf_personalidade_str = ['' for _ in range(10)]

    inf_personalidade_str[0] = ""
    inf_personalidade_str[1] = "O primeiro dos eneatipos é caracterizado por um ego muito focado na disciplina, busca destacar sempre os erros de tudo o que vê e é incapaz de deixar um detalhe sem concertar.\nSão ordenados e têm uma concepção muito forte do que é certo e do que é errado.\nApesar de suas boas intenções, em sua busca pela perfeição, podem ferir os sentimentos alheios ao destacar sempre os detalhes negativos.\nO trabalho psicológico do UM será baseado em encontrar a paz, ser menos auto exigente, cultivar a bondade, aceitar a si mesmo e aos outros."
    inf_personalidade_str[2] = "As pessoas desse eneatipo concentram toda sua atenção nos outros, buscam o amor através de atos ou gestos de ajuda para os outros e geralmente sentem um tipo de ""orgulho"" ao sentir que alguém precisa deles.\nQuerem ser amados e se sentir queridos ao preço que faça falta.\nNão se concentram em suas necessidades e isso pode afetar seu bem-estar pessoal.\nO objetivo de crescimento de um DOIS será aprender a dar amor e deixar de precisar de carinho externo, reconhecer sua humildade e deixar para trás o sentimento de orgulho."
    inf_personalidade_str[3] = "O tipo TRÊS é caracterizado por uma tendência a agir como ele ou ela acredita que os outros querem que ele aja.\nEles se preocupam muitíssimo com a imagem que projetam para os outros e vivem por e para ela.\nO caminho para o bem-estar do tipo TRÊS será orientado a deixar para trás a vaidade e agir de acordo com seus sentimentos e emoções próprias, deixando de focar no que os outros pensam."
    inf_personalidade_str[4] = "Essas pessoas se conectam profundamente com as emoções, têm uma forte necessidade inconsciente de se sentirem amados, de serem únicos e especiais.\nFrequentemente desenvolvem transtornos relacionados com a depressão e tem um profundo sentimento de inferioridade.\nSão o tipo de personalidade mais criativo, mas ao mesmo tempo mais melancólico e pessimista.\nO conselho psicológico para um indivíduo com personalidade QUATRO estará focado em cultivar um sentimento de igualdade em relação aos outros, a autoestima e deixar-se amar."
    inf_personalidade_str[5] = "Aquelas pessoas analíticas, observadoras e perceptivas são geralmente descritas no tipo de personalidade CINCO.\nSeu mundo está em sua cabeça e eles raramente o compartilham, têm uma profunda dificuldade para conectar com as emoções e ainda mais se eles são estrangeiros.\nO caminho para o crescimento de uma pessoa com um eneatipo CINCO será direcionado para fora do isolamento pessoal e compartilhar seus pensamentos e emoções com outras pessoas."
    inf_personalidade_str[6] = "Os indivíduos que são definidos como eneatipo SEIS são aqueles cujo valor principal é a sinceridade e a fidelidade.\nGeralmente são extremamente ansiosos e desconfiados, têm medo do desconhecido de tudo que pode causar algum tipo de dano emocional.\nOs objetivos emocionais do SEIS serão encontrar o valor dentro deles e aprender a confiar em suas atitudes."
    inf_personalidade_str[7] = "Ativos, vivazes, distraídos...os SETE são um eneatipo cheio de energia e desejo de liberdade.\nSão pessoas que fogem da rotina fazendo mil planos para se distrair, buscam constantemente experiências novas e satisfatórias e geralmente vivem sob uma máscara de alegria para evitar conectar com a dor e a realidade quando essa é pouco agradável.\nA dica psicológica que o tipo SETE pode melhorar se baseará na tomada de responsabilidades, a maturidade emocional e a conexão com a realidade."
    inf_personalidade_str[8] = "As personalidades do tipo OITO são caracterizadas por um forte controle sobre seu ambiente e pelo desejo de esconder suas fraquezas a todo custo.\nSão pessoas combativas, agressivas e orientadas para o poder.\nBuscam proteger aqueles indivíduos que eles consideram ""merecedores de proteção"" e tentam impor suas ideias a todo custo.\nPara que um OITO possa crescer emocionalmente é recomendável um trabalho orientado a recuperar a inocência e bondade própria da criança interior, aceitar suas fraquezas e aprender a viver no amor."
    inf_personalidade_str[9] = "As pessoas desse eneatipo são indivíduos tranquilos, mediadores e com tendência a evitar o conflito.\nNecessitam que em seu ambiente reine a paz e a harmonia.\nEles geralmente não enfrentam os outros porque não querem romper essa tranquilidade interna, é por isso que se sentem desconfortáveis com as mudanças e os desafios inesperados.\nOs objetivos recomendados para o tipo de personalidade NOVE estarão relacionados com mostrar suas emoções, aprender a tomar decisões e amar-se, respeitando seus reais desejos."

    caminho_img_fundo_str = ['' for _ in range(10)]

    caminho_img_fundo_str[0] = ""
    caminho_img_fundo_str[1] = "D:\\prog\\img\\perfecionista.png"
    caminho_img_fundo_str[2] = "D:\\prog\\img\\prestativo.png"
    caminho_img_fundo_str[3] = "D:\\prog\\img\\Bem-sucedido.png"
    caminho_img_fundo_str[4] = "D:\\prog\\img\\Individual.png"
    caminho_img_fundo_str[5] = "D:\\prog\\img\\Observador.png"
    caminho_img_fundo_str[6] = "D:\\prog\\img\\Questionador.png"
    caminho_img_fundo_str[7] = "D:\\prog\\img\\Sonhador.png"
    caminho_img_fundo_str[8] = "D:\\prog\\img\\Confrontador.png"
    caminho_img_fundo_str[9] = "D:\\prog\\img\\Pacifista.png"

class App:

    pergunta = ""

    def erro_de_rede(self):
        global rede_quest
        print(rede_quest)
        if rede_quest:
            global pergunta
            pergunta = tk.messagebox.askquestion("Erro de rede", "Não foi possível estabelecer conexão á rede, deseja continuar com o teste?")
            if pergunta == "no":
                self.janela_init.destroy() # acho que destroi tudo exceto o processo
                sys.exit(0) # destroi o processo
            else:
                rede_quest = False

    def cria_xml(self):
        cria = True
        if os.path.exists('resultado.xml'):
            try:
        # Se existir, carregue o arquivo XML existente
                tree = ET.parse('resultado.xml')
                self.dados = tree.getroot()
                cria = False
            except:
                tk.messagebox.showerror("Erro de escrita", "Foi detectado uma possível violação no ficheiro de registro do programa.", detail="O ficheiro sera recriado")
        if cria:
        # Se não existir, crie um novo elemento raiz
            self.dados = ET.Element("dados")
            tree = ET.ElementTree(self.dados)
        return tree

    def escreve_resultado_xml(self, fich_obj, resultado_index, resultado):
        novo_elemento = ET.SubElement(fich_obj, resultado_index)
        for key, value in resultado.items():
            esc_resultado = ET.SubElement(novo_elemento, key)
            esc_resultado.text = str(value)

    def le_registro_xml(self):
        fich_le_xml = ET.parse('resultado.xml')
        const_dados = fich_le_xml.getroot()
        numero_de_dados = len(list(const_dados))
        const_dados_formatados = [['' for _ in range(4)] for _ in range(numero_de_dados)]
        for linha in range(len(list(const_dados))):
            for coluna in range(4):
                const_dados_formatados[linha][coluna] = const_dados[linha][coluna].text
        return const_dados_formatados
    
    # cria e verifica se o ficheiro já existe
    # retona False se o ficheiro já existir
    # rtorna True se o ficheiro foi criado
    def cria_ficheiro(self):
        if os.path.exists("email-cache.txt"):
            return False
        else:
            ficheiro = open("email-cache.txt", "w") # apenas cria ficheiro
            ficheiro.close()
            return True
        
    def le_cache(self, email_str):
        encontrou = False
        email_cache_leitura = open("email-cache.txt", "rt")
        for string in email_cache_leitura:
            if email_str == string:
                encontrou = True # encontrou email na cache local do computador
                break
        email_cache_leitura.close()
        return encontrou

    def mostrar_info(self, inf_personalidade, tit_personalidade, img_path):
        self.botao_info["state"] = "disabled"
        self.botao_menu["state"] = "disabled"
        janela_info = Toplevel(self.janela_init)
        janela_info.protocol("WM_DELETE_WINDOW", lambda : self.repoe_botoes_final(janela_info))
        janela_info.title("Informação sobre a personalidade")
        janela_info.resizable(False, False)
        self.centralizar_janela(janela_info)
        
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

    # codigo copiado que vai ser eliminado no futuro
    def centralizar_janela(self, janela):
        janela_principal = janela.master
        x = int((janela_principal.winfo_width() - janela.winfo_width()) / 3.5)
        y = int((janela_principal.winfo_height() - janela.winfo_height()) / 2.5)
        janela.geometry(f"+{x}+{y}")

    def ver_registro(self, logo):

        winsound.PlaySound("D:\\prog\\img\\zapsplat_multimedia_button_click_bright_003_92100.wav", audio_async) # executa o audio de forma assincrona por causa do elevado tempo de resposta
        
        if not os.path.exists("resultado.xml"):
            tk.messagebox.showinfo("Sem dados", "Não foi detectado nenhum dado no registro, realize um teste")
            return 1
        
        self.janela_reg = Toplevel(self.janela_init)
        self.janela_reg.title("Registro")
        self.janela_reg.resizable(False, False)
        self.janela_reg.iconphoto(False, logo)
        self.centralizar_janela(self.janela_reg)
        

        self.botao_init["state"] = "disabled"
        self.botao_registo["state"] = "disabled"

        self.janela_reg.protocol("WM_DELETE_WINDOW", self.repoe_botoes_init)

        colunas = ('Nome', 'Email', 'Resultado', 'Data')

        grelha = ttk.Treeview(self.janela_reg, columns=colunas, show='headings')

        rolagem = Scrollbar(self.janela_reg, orient="vertical", command=grelha.yview)
        rolagem.pack(side="right", fill="y")

        grelha.config(yscrollcommand=rolagem.set)

        grelha.heading('Nome', text='Nome')
        grelha.heading('Email', text='Email')
        grelha.heading('Resultado', text='Resultado')
        grelha.heading('Data', text='Data')

        dados_formatados = self.le_registro_xml()

        for linha in range(len(list(dados_formatados))):
            grelha.insert("", tk.END, values=(dados_formatados[linha][0], dados_formatados[linha][1], dados_formatados[linha][2], dados_formatados[linha][3]))
        
        grelha.pack()
        
    def repoe_botoes_init(self):
        self.botao_init["state"] = "normal"
        self.botao_registo["state"] = "normal"
        self.janela_reg.destroy()

    def repoe_botoes_final(self, janela_inf):
        self.botao_info["state"] = "normal"
        self.botao_menu["state"] = "normal"
        janela_inf.destroy()

    # atributos globais
    resultado_do_user = 0
    interrupted_rede = False

    def verifica_rede(self):
        global interrupted_rede
        while not interrupted_rede:
            self.mutex.acquire()
            try:
                _ = requests.get("http://www.google.com", timeout=5)
                self.rede = True
            except:
                self.rede = False
            finally:
                if self.mutex.locked():
                    self.mutex.release()
            time.sleep(0.1)

    # informa ao utilizador de forma paralela que a validação de email esta a ser executada
    def inf_teste_email(self):
            self.janela_inf_email = tk.Toplevel()
            self.janela_inf_email.withdraw()
            
            tk.messagebox.showinfo("Verificando email", "A verificação de email está a ser executada, esta operação pode demorar dependendo da sua rede.")

    def __init__ (self, janela_init, tipos, back):
        if back:
            winsound.PlaySound("D:\\prog\\img\\zapsplat_multimedia_button_click_bright_003_92100.wav", winsound.SND_FILENAME | winsound.SND_ASYNC) # executa o audio de forma assincrona por causa do elevado tempo de resposta
            self.botao_menu.destroy()
            self.botao_info.destroy()
            self.img_final.close()
            self.label_final.destroy()
            self.Resultado.destroy()
        self.janela_init = janela_init
        self.tipos = tipos
        self.janela_init.title("Teste de personalidade")
        self.janela_init.geometry("1920x1080")

        self.imagem = Image.open("D:\\prog\\img\\fundo_f3.png")
        self.imagem.thumbnail((1920, 860))
        self.imagem_tk = ImageTk.PhotoImage(self.imagem)
        
        self.label1 = Label(self.janela_init, image=self.imagem_tk)
        self.label1.pack()

        self.label1.imagem = self.imagem_tk

        self.imagem_cinzento = Image.open("D:\\prog\\img\\cinzento.jpg")
        self.imagem_cinzento.thumbnail((1920, 1080))
        self.imagem_cinzento_tk = ImageTk.PhotoImage(self.imagem_cinzento)
        
        self.label_cinzento = Label(self.janela_init, image=self.imagem_cinzento_tk)
        self.label_cinzento.pack()

        self.label_cinzento.imagem = self.imagem_cinzento_tk

        self.imagem_rosa = Image.open("D:\\prog\\img\\rosa.jpg")
        self.imagem_rosa.thumbnail((1920, 1080))
        self.imagem_rosa_tk = ImageTk.PhotoImage(self.imagem_rosa)
        
        self.label_rosa = Label(self.janela_init, image=self.imagem_rosa_tk)
        self.label_rosa.pack()

        self.label_rosa.imagem = self.imagem_rosa_tk

        self.imagem_azul = Image.open("D:\\prog\\img\\azul.jpg")
        self.imagem_azul.thumbnail((1920, 1080))
        self.imagem_azul_tk = ImageTk.PhotoImage(self.imagem_azul)
        
        self.label_azul = Label(self.janela_init, image=self.imagem_azul_tk)
        self.label_azul.pack()

        self.label_azul.imagem = self.imagem_azul_tk

        imagem_logo = Image.open("D:\\prog\\img\\logo.png")
        logo = ImageTk.PhotoImage(imagem_logo)

        imagem_botao = Image.open("D:\\prog\\img\\botao_f.png")
        imagem_botao_f = ImageTk.PhotoImage(imagem_botao)

        imagem_reg = Image.open("D:\\prog\\img\\reg.png")
        imagem_reg_f = ImageTk.PhotoImage(imagem_reg)

        # Defina a imagem como ícone
        self.janela_init.iconphoto(False, logo)
        self.mensagem_principal = tk.Label()
        Mensagem_nome = tk.Label(text="Nome:", bg="white", compound="center", font=('Arial Black', 10))
        Mensagem_email = tk.Label(text="Email:", bg="white", font=('Arial Black', 10))
        nome = tk.Entry(width=40, exportselection=True)
        email_entry = tk.Entry(width=40, exportselection=True)
        self.botao_registo = tk.Button(janela_init, image=imagem_reg_f, width=180, height=30, command=partial(self.ver_registro, logo))
        self.botao_init = tk.Button(janela_init, image=imagem_botao_f, width=250, height=50, command=partial(self.verifica, nome, Mensagem_nome, email_entry, Mensagem_email, self.label1))
        self.botao_init.image = imagem_botao_f
        self.botao_registo.image = imagem_reg_f
        Mensagem_nome.place(x=520, y=230)
        nome.place(x=520, y=260)
        Mensagem_email.place(x=520, y=290)
        email_entry.place(x=520, y=320)
        self.botao_init.place(x=520, y=360)
        self.botao_registo.place(x=560, y=430)
    
    def verifica(self, id, mensagem, email, mensagem_email, img_fundo):
        winsound.PlaySound("D:\\prog\\img\\zapsplat_multimedia_button_click_bright_003_92100.wav", winsound.SND_FILENAME | winsound.SND_ASYNC) # executa o audio de forma assincrona por causa do elevado tempo de resposta
        global interrupted_rede
        interrupted_rede = False
        self.email_check = email.get()
        self.nome_id = id.get()
        self.rede = True
        self.pergunta = ""
        self.mutex = threading.Lock()
        econtrou = False
        tarefa_rede = threading.Thread(target=self.verifica_rede)
        tarefa_rede.start()
        if self.nome_id == "":
            tk.messagebox.showerror("Preencha o campo nome", "É obrigatorio introduzor o nome")
            id.config(bg="#FFC0CB")
            return 1
        elif self.email_check == "":
            tk.messagebox.showerror("Preencha o campo email", "É obrigatorio introduzor o email")
            email.config(bg="#FFC0CB")
            return 1
        elif self.cria_ficheiro() == False:
            econtrou = self.le_cache(self.email_check + "\n")

        self.mutex.acquire()
        # sem o acesso á rede não podemos validar o email
        if econtrou == False and self.rede == True:
            self.mutex.release()
            #tarefa_inf = threading.Thread(target=self.inf_teste_email)
            #tarefa_inf.start()
            
            
            
            if not validate_email(email_address=self.email_check):
                #self.janela_inf_email.destroy()
                self.mutex.acquire()
                if self.rede == True:
                    tk.messagebox.showerror("Email invalido", "O email introduzido é invlido ou não existe, reescreva")
                    email.config(bg="#FFC0CB")
                    interrupted_rede = True
                    self.mutex.release()
                    return 1
                else:
                    self.pergunta = tk.messagebox.askquestion("Erro de rede", "Não foi possível estabelecer conexão á rede, deseja continuar com o teste?")
                    self.mutex.release()
            else: # se o email estiver correto mas o utilizador não tiver o acessso a rede o email não sera guardado no ficheiro de cache
                ficheiro_cache_escrita = open("email-cache.txt", "a")
                ficheiro_cache_escrita.write(self.email_check + "\n")
                ficheiro_cache_escrita.close()
        elif self.rede == False:
            self.pergunta = tk.messagebox.askquestion("Erro de rede", "Não foi possível estabelecer conexão á rede, deseja continuar com o teste?")

        if self.mutex.locked():
            self.mutex.release()
        interrupted_rede = True
        if self.pergunta == "no":
            return 1

        self.botao_init.destroy()
        id.destroy()
        mensagem.destroy()
        email.destroy()
        mensagem_email.destroy()
        self.botao_registo.destroy()
        self.imagem.close()
        img_fundo.destroy()
        self.init_cinzento()
    
    def init_cinzento(self):
        self.mensagem_principal.config(text="Escolha uma das opções", bg="#808080", font=("Arial", 25, "bold"), justify="center")
        self.imagem_botao_pergunta = Image.open("D:\\prog\\img\\botao_c.png")
        self.imagem_botao_pergunta_tk = ImageTk.PhotoImage(self.imagem_botao_pergunta)
        self.Botao1 = tk.Button(self.janela_init, image=self.imagem_botao_pergunta_tk, text="Direto, Frontal, Impaciente com ritmo de outros, Assertivo", compound="center", width=580, height=40, command=partial(self.cinzento2, 8))
        self.Botao1.image = self.imagem_botao_pergunta_tk
        self.Botao2 = tk.Button(self.janela_init, image=self.imagem_botao_pergunta_tk, text="Analítico, Observador, Frio Emocionalmente, Independente", compound="center", width=580, height=40, command=partial(self.cinzento2, 5))
        self.Botao2.image = self.imagem_botao_pergunta_tk
        self.Botao3 = tk.Button(self.janela_init, image=self.imagem_botao_pergunta_tk, text="Empenhado, Habilidade nas relações, Organizado, Voluntarioso", compound="center", width=580, height=40, command=partial(self.cinzento2, 2))
        self.Botao3.image = self.imagem_botao_pergunta_tk
        self.Botao1.place(x=50, y=450)
        self.Botao2.place(x=350, y=300)
        self.Botao3.place(x=650, y=450)
        self.mensagem_principal.place(x=450,y=150)

    def cinzento2(self, resp_num):
        winsound.PlaySound("D:\\prog\\img\\zapsplat_multimedia_button_click_bright_003_92100.wav", winsound.SND_FILENAME | winsound.SND_ASYNC) # executa o audio de forma assincrona por causa do elevado tempo de resposta
        self.tipos.resp[0] = resp_num
        self.Botao1.config(command=partial(self.cinzento3, 6), text="Questionador, Precavido, Organizado, Antecipa os vários cenários")
        self.Botao2.config(command=partial(self.cinzento3, 7), text="Otimista, Entusiasta, Criativo, Foco em multi-opções")
        self.Botao3.config(command=partial(self.cinzento3, 1), text="Perfeccionismo, Disciplinado, Foco no detalhe Rígido e determinado")

    def cinzento3(self, resp_num):
        winsound.PlaySound("D:\\prog\\img\\zapsplat_multimedia_button_click_bright_003_92100.wav", winsound.SND_FILENAME | winsound.SND_ASYNC) # executa o audio de forma assincrona por causa do elevado tempo de resposta
        self.tipos.resp[1] = resp_num
        self.Botao1.config(command=partial(self.cinzento4, 3), text="Competitivo, Confiante, Foco no sucesso, Objetivo")
        self.Botao2.config(command=partial(self.cinzento4, 4), text="Sonhador, Intenso, Emotivo, Romântico")
        self.Botao3.config(command=partial(self.cinzento4, 9), text="Pacificador, Flexível, Calmo e cordial, Dificuldade em dizer não")

    def cinzento4(self, resp_num):
        winsound.PlaySound("D:\\prog\\img\\zapsplat_multimedia_button_click_bright_003_92100.wav", winsound.SND_FILENAME | winsound.SND_ASYNC) # executa o audio de forma assincrona por causa do elevado tempo de resposta
        self.tipos.resp[2] = resp_num
        self.Botao1.config(command=partial(self.cinzento5, 7), text="Otimista, Entusiasta, Criativo, Foco em multi-opções")
        self.Botao2.config(command=partial(self.cinzento5, 3), text="Competitivo, Confiante, Foco no sucesso, Objetivo")
        self.Botao3.config(command=partial(self.cinzento5, 9), text="Pacificador, Flexível, Calmo e cordial, Dificuldade em dizer não")

    def cinzento5(self, resp_num):
        winsound.PlaySound("D:\\prog\\img\\zapsplat_multimedia_button_click_bright_003_92100.wav", winsound.SND_FILENAME | winsound.SND_ASYNC) # executa o audio de forma assincrona por causa do elevado tempo de resposta
        self.tipos.resp[3] = resp_num
        self.Botao1.config(command=partial(self.cinzento6, 4), text="Sonhador, Intenso, Emotivo, Romântico")
        self.Botao2.config(command=partial(self.cinzento6, 1), text="Perfeccionismo, Disciplinado, Foco no detalhe Rígido e determinado")
        self.Botao3.config(command=partial(self.cinzento6, 8), text="Direto, Frontal, Impaciente com ritmo de outros, Assertivo")

    def cinzento6(self, resp_num):
        winsound.PlaySound("D:\\prog\\img\\zapsplat_multimedia_button_click_bright_003_92100.wav", winsound.SND_FILENAME | winsound.SND_ASYNC) # executa o audio de forma assincrona por causa do elevado tempo de resposta
        self.tipos.resp[4] = resp_num
        self.Botao1.config(command=partial(self.cinzento7, 5), text="Analítico, Observador, Frio Emocionalmente, Independente")
        self.Botao2.config(command=partial(self.cinzento7, 2), text="Empenhado, Habilidade nas relações, Organizado, Voluntarioso")
        self.Botao3.config(command=partial(self.cinzento7, 6), text="Questionador, Precavido, Organizado, Antecipa os vários cenários")

    def cinzento7(self, resp_num):
        winsound.PlaySound("D:\\prog\\img\\zapsplat_multimedia_button_click_bright_003_92100.wav", winsound.SND_FILENAME | winsound.SND_ASYNC) # executa o audio de forma assincrona por causa do elevado tempo de resposta
        self.tipos.resp[5] = resp_num
        self.Botao1.config(command=partial(self.cinzento8, 7), text="Otimista, Entusiasta, Criativo, Foco em multi-opções")
        self.Botao2.config(command=partial(self.cinzento8, 9), text="Pacificador, Flexível, Calmo e cordial, Dificuldade em dizer não")
        self.Botao3.config(command=partial(self.cinzento8, 2), text="Empenhado, Habilidade nas relações, Organizado, Voluntarioso")
    
    def cinzento8(self, resp_num):
        winsound.PlaySound("D:\\prog\\img\\zapsplat_multimedia_button_click_bright_003_92100.wav", winsound.SND_FILENAME | winsound.SND_ASYNC) # executa o audio de forma assincrona por causa do elevado tempo de resposta
        self.tipos.resp[6] = resp_num
        self.Botao1.config(command=partial(self.cinzento9, 6), text="Questionador, Precavido, Organizado, Antecipa os vários cenários")
        self.Botao2.config(command=partial(self.cinzento9, 8), text="Direto, Frontal, Impaciente com ritmo de outros, Assertivo")
        self.Botao3.config(command=partial(self.cinzento9, 4), text="Sonhador, Intenso, Emotivo, Romântico")
    
    def cinzento9(self, resp_num):
        winsound.PlaySound("D:\\prog\\img\\zapsplat_multimedia_button_click_bright_003_92100.wav", winsound.SND_FILENAME | winsound.SND_ASYNC) # executa o audio de forma assincrona por causa do elevado tempo de resposta
        self.tipos.resp[7] = resp_num
        self.Botao1.config(command=partial(self.cinzento10, 5), text="Analítico, Observador, Frio Emocionalmente, Independente")
        self.Botao2.config(command=partial(self.cinzento10, 1), text="Perfeccionismo, Disciplinado, Foco no detalhe Rígido e determinado")
        self.Botao3.config(command=partial(self.cinzento10, 3), text="Competitivo, Confiante, Foco no sucesso, Objetivo")
    
    def cinzento10(self, resp_num):
        winsound.PlaySound("D:\\prog\\img\\zapsplat_multimedia_button_click_bright_003_92100.wav", winsound.SND_FILENAME | winsound.SND_ASYNC) # executa o audio de forma assincrona por causa do elevado tempo de resposta
        self.tipos.resp[8] = resp_num
        self.Botao1.config(command=partial(self.cinzento11, 9), text="Pacificador, Flexível, Calmo e cordial, Dificuldade em dizer não")
        self.Botao2.config(command=partial(self.cinzento11, 8), text="Direto, Frontal, Impaciente com ritmo de outros, Assertivo")
        self.Botao3.config(command=partial(self.cinzento11, 3), text="Competitivo, Confiante, Foco no sucesso, Objetivo")
    
    def cinzento11(self, resp_num):
        winsound.PlaySound("D:\\prog\\img\\zapsplat_multimedia_button_click_bright_003_92100.wav", winsound.SND_FILENAME | winsound.SND_ASYNC) # executa o audio de forma assincrona por causa do elevado tempo de resposta
        self.tipos.resp[9] = resp_num
        self.Botao1.config(command=partial(self.cinzento12, 4), text="Sonhador, Intenso, Emotivo, Romântico")
        self.Botao2.config(command=partial(self.cinzento12, 7), text="Otimista, Entusiasta, Criativo, Foco em multi-opções")
        self.Botao3.config(command=partial(self.cinzento12, 1), text="Perfeccionismo, Disciplinado, Foco no detalhe Rígido e determinado")
    
    def cinzento12(self, resp_num):
        winsound.PlaySound("D:\\prog\\img\\zapsplat_multimedia_button_click_bright_003_92100.wav", winsound.SND_FILENAME | winsound.SND_ASYNC) # executa o audio de forma assincrona por causa do elevado tempo de resposta
        self.tipos.resp[10] = resp_num
        self.Botao1.config(command=partial(self.init_fase_rosa, 2), text="Empenhado, Habilidade nas relações, Organizado, Voluntarioso")
        self.Botao2.config(command=partial(self.init_fase_rosa, 6), text="Questionador, Precavido, Organizado, Antecipa os vários cenários")
        self.Botao3.config(command=partial(self.init_fase_rosa, 5), text="Analítico, Observador, Frio Emocionalmente, Independente")
    
    def init_fase_rosa(self, resp_num):
        winsound.PlaySound("D:\\prog\\img\\zapsplat_multimedia_button_click_bright_003_92100.wav", winsound.SND_FILENAME | winsound.SND_ASYNC) # executa o audio de forma assincrona por causa do elevado tempo de resposta
        self.imagem_cinzento.close()
        self.label_cinzento.destroy()
        self.mensagem_principal["bg"] = "pink"
        self.tipos.resp[11] = resp_num
        self.imagem_botao_pergunta.close()
        self.imagem_botao_pergunta = Image.open("D:\\prog\\img\\botao_r.png")
        self.imagem_botao_pergunta_tk = ImageTk.PhotoImage(self.imagem_botao_pergunta)
        self.Botao1.config(command=partial(self.rosa_2, self.tipos.resp[0], 0, 3), image=self.imagem_botao_pergunta_tk,text=self.tipos.tipo_rosa_str[self.tipos.resp[0]], width=580)
        self.Botao2.config(command=partial(self.rosa_2, self.tipos.resp[1], 0, 3), image=self.imagem_botao_pergunta_tk,text=self.tipos.tipo_rosa_str[self.tipos.resp[1]], width=580)
        self.Botao3.config(command=partial(self.rosa_2, self.tipos.resp[2], 0, 3), image=self.imagem_botao_pergunta_tk,text=self.tipos.tipo_rosa_str[self.tipos.resp[2]], width=580)

    def rosa_2(self, resp_num, index_resp, index_text):
        winsound.PlaySound("D:\\prog\\img\\zapsplat_multimedia_button_click_bright_003_92100.wav", winsound.SND_FILENAME | winsound.SND_ASYNC) # executa o audio de forma assincrona por causa do elevado tempo de resposta
        self.tipos.fase_2_resp[index_resp] = resp_num
        if index_text == 12:
            self.verifica_repeticao() # parametro apenas de trensporte
        else:
            self.Botao1.config(command=partial(self.rosa_2, self.tipos.resp[index_text], index_resp+1, index_text+3), text=self.tipos.tipo_rosa_str[self.tipos.resp[index_text]])
            self.Botao2.config(command=partial(self.rosa_2, self.tipos.resp[index_text+1], index_resp+1, index_text+3), text=self.tipos.tipo_rosa_str[self.tipos.resp[index_text+1]])
            self.Botao3.config(command=partial(self.rosa_2, self.tipos.resp[index_text+2], index_resp+1, index_text+3), text=self.tipos.tipo_rosa_str[self.tipos.resp[index_text+2]])

    def verifica_repeticao(self):
        winsound.PlaySound("D:\\prog\\img\\zapsplat_multimedia_button_click_bright_003_92100.wav", winsound.SND_FILENAME | winsound.SND_ASYNC) # executa o audio de forma assincrona por causa do elevado tempo de resposta
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

    def fase_rosa2_1(self):
        winsound.PlaySound("D:\\prog\\img\\zapsplat_multimedia_button_click_bright_003_92100.wav", winsound.SND_FILENAME | winsound.SND_ASYNC) # executa o audio de forma assincrona por causa do elevado tempo de resposta
        self.Botao1.config(command=partial(self.fase_rosa2_2, self.tipos.fase_2_resp[0]), text=self.tipos.tipo_rosa_str[self.tipos.fase_2_resp[0]])
        self.Botao2.config(command=partial(self.fase_rosa2_2, self.tipos.fase_2_resp[1]), text=self.tipos.tipo_rosa_str[self.tipos.fase_2_resp[1]])
        self.Botao3.config(command=partial(self.fase_rosa2_2, self.tipos.fase_2_resp[2]), text=self.tipos.tipo_rosa_str[self.tipos.fase_2_resp[2]])
        
    def fase_rosa2_2(self, resp_num):
        winsound.PlaySound("D:\\prog\\img\\zapsplat_multimedia_button_click_bright_003_92100.wav", winsound.SND_FILENAME | winsound.SND_ASYNC) # executa o audio de forma assincrona por causa do elevado tempo de resposta
        self.tipos.fase_2_resp[0] = resp_num
        self.Botao1.config(command=partial(self.leve_verificação, self.tipos.fase_2_resp[1]), text=self.tipos.tipo_rosa_str[self.tipos.fase_2_resp[1]])
        self.Botao2.config(command=partial(self.leve_verificação, self.tipos.fase_2_resp[2]), text=self.tipos.tipo_rosa_str[self.tipos.fase_2_resp[2]])
        self.Botao3.config(command=partial(self.leve_verificação, self.tipos.fase_2_resp[3]), text=self.tipos.tipo_rosa_str[self.tipos.fase_2_resp[3]])

    def leve_verificação(self, resp_num):
        winsound.PlaySound("D:\\prog\\img\\zapsplat_multimedia_button_click_bright_003_92100.wav", winsound.SND_FILENAME | winsound.SND_ASYNC) # executa o audio de forma assincrona por causa do elevado tempo de resposta
        self.tipos.fase_2_resp[1] = resp_num
        contador = 2
        while 1:
            if self.tipos.fase_2_resp[0] == self.tipos.fase_2_resp[1]:
                self.tipos.fase_2_resp[1] = self.tipos.fase_2_resp[contador] # solução para um pequeno bug
                contador += 1
            else:
                break
        self.init_azul()

    def init_azul(self):
        self.label_rosa.destroy()
        self.imagem_rosa.close()
        self.mensagem_principal["bg"] = "blue"
        self.imagem_botao_pergunta.close()
        self.imagem_botao_pergunta = Image.open("D:\\prog\\img\\botao_a.png")
        self.imagem_botao_pergunta_tk = ImageTk.PhotoImage(self.imagem_botao_pergunta)
        self.Botao2.destroy()
        self.Botao1.config(command=partial(self.resultado_final, self.tipos.fase_2_resp[0]), image=self.imagem_botao_pergunta_tk,text=self.tipos.tipo_azul_str[self.tipos.fase_2_resp[0]])
        self.Botao3.config(command=partial(self.resultado_final, self.tipos.fase_2_resp[1]), image=self.imagem_botao_pergunta_tk,text=self.tipos.tipo_azul_str[self.tipos.fase_2_resp[1]])

    def resultado_final(self, resp_num):
        winsound.PlaySound("D:\\prog\\img\\zapsplat_multimedia_button_click_bright_003_92100.wav", winsound.SND_FILENAME | winsound.SND_ASYNC) # executa o audio de forma assincrona por causa do elevado tempo de resposta
        self.label_azul.destroy()
        self.imagem_azul.close()
        self.mensagem_principal.destroy()
        self.img_final = Image.open("D:\\prog\\img\\resultado.png")
        self.img_final_tk = ImageTk.PhotoImage(self.img_final)
        img_menu = Image.open("D:\\prog\\img\\menu.png")
        img_menu_tk = ImageTk.PhotoImage(img_menu)
        img_inf = Image.open("D:\\prog\\img\\mais.png")
        img_inf_tk = ImageTk.PhotoImage(img_inf)
        self.label_final = Label(self.janela_init, image=self.img_final_tk)
        self.label_final.pack()

        self.label_final.imagem = self.img_final_tk
        self.Botao3.destroy()
        self.Botao1.destroy()

        self.resultado_do_user = self.tipos.resultado_str[resp_num]
        self.Resultado = tk.Label(bg="purple", font=("Arial", 30, "bold"), text="O seu tipo é " + str(resp_num) + "-" + self.tipos.resultado_str[resp_num]) 
        self.botao_menu = tk.Button(width=200, height=40, image=img_menu_tk, command=partial(self.__init__, self.janela_init, self.tipos, 1))
        self.botao_info = tk.Button(width=200, height=60, image=img_inf_tk, command=partial(self.mostrar_info, self.tipos.inf_personalidade_str[resp_num], self.resultado_do_user, self.tipos.caminho_img_fundo_str[resp_num]))
        self.botao_menu.image = img_menu_tk
        self.botao_info.image = img_inf_tk
        self.botao_menu.place(x=540, y=350)
        self.botao_info.place(x=540, y=410)
        self.Resultado.place(x=430,y=150)
        tempo = strftime("%d/%m/%Y %H:%M:%S", gmtime(time.time()))
        fich_xml = self.cria_xml()
        num_resultados = len(list(self.dados))
        resultado_lista = {"nome": self.nome_id, "email": self.email_check, "resultado": self.resultado_do_user, "tempo": tempo}
        self.escreve_resultado_xml(self.dados, "teste" + str(num_resultados), resultado_lista)
        fich_xml.write("resultado.xml")

janela = Tk()
personalidades = tipos_personalidade()
app = App(janela, personalidades, 0)
janela.mainloop()
