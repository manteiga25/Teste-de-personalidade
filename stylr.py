import psycopg2
from urllib.parse import urlparse
import random
import time
from time import gmtime, strftime

def conectar_banco_de_dados():
    # URL fornecido pelo ElephantSQL
    url = "postgres://tgzkwyzy:pMRrG6CmTqWzwtXGWPsj3R9ohD82OXf6@surus.db.elephantsql.com/tgzkwyzy"

    # Parseie a URL para extrair as informações de conexão
    parsed_url = urlparse(url)
    
    # Extraia as informações de conexão do URL
    user = parsed_url.username
    password = parsed_url.password
    host = parsed_url.hostname
    port = parsed_url.port
    database = parsed_url.path.lstrip('/')
    # Conecte-se ao banco de dados remoto
    conexao = psycopg2.connect(
        host="surus.db.elephantsql.com",
        port=None,
        user="tgzkwyzy",
        password="pMRrG6CmTqWzwtXGWPsj3R9ohD82OXf6",
        database="tgzkwyzy"
    )
    return conexao


def inserir_usuario():
    conexao = conectar_banco_de_dados()
    cursor = conexao.cursor()

    nome = ""
    for i in range(100):
        for j in range(20):
            nome += chr(random.randrange(65, 88))
        resultado = random.randrange(1, 10)
        data = strftime("%d/%m/%Y %H:%M:%S", gmtime(time.time()))
        comando_sql = '''
            INSERT INTO testes (nome, resultado, data) 
            VALUES (%s, %s, %s)
        '''
    # Executa o comando SQL para inserir um novo usuário
        cursor.execute(comando_sql, (nome, resultado, data))
        nome = ""

    # Confirma a transação e fecha a conexão
    conexao.commit()
    conexao.close()
inserir_usuario()
