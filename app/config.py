# Objeto de conexão para encontrar o servidor, sql logon e efetivar a conexão
from app import app
from flaskext.mysql import MySQL
from flask_basicauth import BasicAuth
import os
from  dotenv  import  load_dotenv, find_dotenv

load_dotenv (find_dotenv())

app.config['BASIC_AUTH_USERNAME'] = '' #insira usuário
app.config['BASIC_AUTH_PASSWORD'] = '' #insira senha

auth = BasicAuth(app)


mysql = MySQL()

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = '' #insira o nome do seu usuário
app.config['MYSQL_DATABASE_PASSWORD'] = '' #insira a sua senha do banco
app.config['MYSQL_DATABASE_DB'] = '' #insira o nome do seu banco
app.config['MYSQL_DATABASE_HOST'] = '' #insira o nome do seu host


mysql.init_app(app)

