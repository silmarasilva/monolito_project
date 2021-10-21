import pymysql
from app import app
from config import mysql, auth
from flask import jsonify, Response, flash,request
from flask_debug import Debug
from flask_basicauth import BasicAuth

basic_auth = auth

# Adicionando um registro - POST
# Não precisa passaro id na rota e banco não aceita cursos duplicados.
@app.route('/cursos', methods=['POST'])
@basic_auth.required
def add_curso():
    try:
        _json = request.get_json(force = True)        
        _nome = _json['nome']
        _descricao = _json['descricao']
        _carga = _json['carga']
        _totaulas = _json['totaulas']
        _ano = _json['ano']
        _preco = _json['preco']
        _ativo = _json['ativo']

        if _nome and _descricao and _carga and _totaulas and _ano and _preco and _ativo and request.method == 'POST':
            sqlQuery = "INSERT INTO db_produtos.tbl_cursos (nome, descricao, carga, totaulas, ano, preco, ativo ) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            bindData = (_nome, _descricao, _carga, _totaulas, _ano, _preco, _ativo)
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)         
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify('Curso adicionado com sucesso!')
            response.status_code = 200
            return response
        else:
            return not_found()
    except Exception as error:
        print(error)
    finally:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.close()
        conn.close()

# Retornando todos os registros - GET
@app.route('/cursos', methods=['GET'])
#@basic_auth.required
def get_cursos():
    try:
        print (request)
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute ("SELECT idCurso, nome, descricao, carga, totaulas, ano, preco, ativo FROM db_produtos.tbl_cursos")
        userRows = cursor.fetchall()
        response = jsonify(userRows)
        response.status_code == 200
        return response   
    except Exception as error:
        print(error)
    finally:
        cursor.close() 
        conn.close()

# Retornando o registro de um ID específico - GET(id)
@app.route('/cursos/<int:id>',  methods=['GET'])
@basic_auth.required
def id_curso(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute ("SELECT idCurso, nome, descricao, carga, totaulas, ano, preco, ativo FROM db_produtos.tbl_cursos WHERE idCurso =%s", id)
        userRow = cursor.fetchone()
        if not userRow:
            return Response('Curso não cadastrado', status=404)
        print (type(userRow))
        response = jsonify(userRow)
        response.status_code == 200
        return response          
    except Exception as error:
        return error
    finally:
        cursor.close()
        conn.close()

# Alterando algum curso - PUT
# No put, precisa passar o ID na rota, que é o id do curso, mas no body eu posso manter o mesmo, ou colocar um número novo, caso queira alterar id do curso.
@app.route('/cursos/<int:id>', methods=['PUT'])
@basic_auth.required
def update_curso(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        _json = request.get_json(force = True)
        _idCurso = _json['idCurso']
        _nome = _json['nome']
        _descricao = _json['descricao']
        _carga = _json['carga']
        _totaulas = _json['totaulas']
        _ano = _json['ano']
        _preco = _json['preco']
        _ativo = _json['ativo']        
        if  _nome and _descricao and _carga and _totaulas and _ano and _preco and _ativo and _idCurso and request.method == 'PUT':
            sqlQuery = "SELECT * FROM db_produtos.tbl_cursos WHERE idCurso=%s"
            cursor.execute(sqlQuery, id)
            select = cursor.fetchone()
            if not select:
                return Response('Curso não cadastrado', status=400)
            sqlQuery = "UPDATE db_produtos.tbl_cursos SET nome=%s, descricao=%s, carga=%s, totaulas=%s, ano=%s, preco=%s, ativo=%s, idCurso=%s WHERE idCurso=%s"
            bindData = (_nome, _descricao, _carga, _totaulas, _ano, _preco, _ativo, _idCurso, id)
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


# Deletando algum curso (DELETE)
@app.route('/cursos/<int:idCurso>', methods=['DELETE'])
@basic_auth.required
def delete_curso(idCurso):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sqlQuery = "SELECT * FROM db_produtos.tbl_cursos WHERE idCurso=%s"
        cursor.execute(sqlQuery, idCurso)
        select = cursor.fetchone()
        if not select:
            return Response('Curso não cadastrado', status=400)
        cursor.execute("DELETE FROM db_produtos.tbl_cursos WHERE idCurso =%s", (idCurso))
        conn.commit()
        respone = jsonify('Curso deletado com sucesso!')
        respone.status_code = 200
        return respone
    except Exception as error:
        print(error)
    finally:
        cursor.close()
        conn.close()


@app.route('/cursos/status/<int:idCurso>', methods = ['GET'])
@basic_auth.required
def curso_status (idCurso):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        status=cursor.execute ("SELECT ativo FROM db_produtos.tbl_cursos WHERE idCurso=%s", idCurso)
        userRow = cursor.fetchall()
        print (userRow)
        if not userRow:
            return Response('Curso não cadastrado.'), 404
        if userRow == [{'ativo': 'N'}]:
            return ('Curso indisponível.'), 404
        if userRow == [{'ativo': 'S'}]:
            return ('Curso disponível'), 200
        response = jsonify(userRow)        
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