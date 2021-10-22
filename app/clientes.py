import pymysql
from app import app
from config import mysql, auth
from flask import jsonify, Response, flash, request
from flask_debug import Debug
from flask_basicauth import BasicAuth

basic_auth = auth

# Adicionando um registro - POST
# Indicar o número do id do cliente no body ou não colocar o campo id no body
@app.route('/clientes', methods=['POST'])
@basic_auth.required
def add_user():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        _json = request.get_json(force = True)        
        _nome = _json['nome']
        _cpf = _json['cpf']
        _email = _json['email']
        _telefone = _json['telefone']
        _senha = _json['senha']

        if _nome and _cpf and _email and _telefone and _senha and request.method == 'POST':
            sqlQuery = "INSERT INTO db_clientes.tbl_clientes (nome, cpf, email, telefone, senha) VALUES (%s,%s,%s,%s,%s)"
            bindData = (_nome, _cpf, _email, _telefone, _senha)
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)         
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify('Cliente adicionado com sucesso!')
            response.status_code = 200
            return response
        else:
            return not_found()
    except Exception as error:
        print(error)
    finally:
        cursor.close()
        conn.close()

# Retornando todos os registros GET
@app.route('/clientes', methods=['GET'])
@basic_auth.required
def get_user():
    try:
        print (request)
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute ("SELECT id, nome, cpf, email, telefone, senha FROM db_clientes.tbl_clientes")
        userRows = cursor.fetchall()
        response = jsonify(userRows)
        response.status_code == 200
        return response     
    
    except Exception as error:
        print(error)
    finally:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.close() 
        conn.close()

# Retornando o registro de um ID específico - GET(ID)
@app.route('/clientes/<int:id>',  methods=['GET'])
@basic_auth.required
def id_user(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute ("SELECT id, nome, cpf, email, telefone, senha FROM db_clientes.tbl_clientes WHERE id =%s", id)
        userRow = cursor.fetchone()
        if not userRow:
            return Response('Usuário não cadastrado', status=404)
        response = jsonify(userRow)
        response.status_code == 200
        return response          
    except Exception as error:
        print (error)
    finally:
        cursor.close()
        conn.close()

# Alterando algum registro - PUT
@app.route('/clientes', methods=['PUT'])
@basic_auth.required
def update_user():
    try:
        _json = request.get_json(force = True)
        _id = _json['id']
        _nome = _json['nome']
        _cpf = _json['cpf']
        _email = _json['email']
        _telefone = _json['telefone']
        _senha = _json['senha'] 
        if _nome and _cpf and _email and _telefone and _senha and _id and request.method == 'PUT':
            sqlQuery = "UPDATE db_clientes.tbl_clientes SET nome=%s, cpf=%s, email=%s, telefone=%s, senha=%s WHERE id=%s"
            bindData = (_nome, _cpf, _email, _telefone, _senha, _id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify('Dados alterados com sucesso!')
            response.status_code = 200
            return response
        else:
            return not_found()	
    except Exception as error:
        print(error)
    finally:
        cursor.close()
        conn.close()

# Deletando algum registro - DELETE
@app.route('/clientes/<int:id>', methods=['DELETE'])
@basic_auth.required
def delete_user(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM db_clientes.tbl_clientes WHERE id =%s", (id,))
        conn.commit()
        response = jsonify('Cliente deletado com sucesso!')
        response.status_code = 200
        return response
    except Exception as error:
        print(error)
    finally:
        cursor.close()
        conn.close()


@app.errorhandler(404)
@basic_auth.required
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == "__main__":
    app.run(debug=True)