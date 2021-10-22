import pymysql
from app import app
from config import mysql, auth
from flask import jsonify, Response, flash, request
from flask_debug import Debug
from mysql.connector import Error
from flask_basicauth import BasicAuth
import requests

basic_auth = auth


# Adicionando um registro
# Não é necessário passar o ID da compra, pois é AI
@app.route('/cliente/compras', methods=['POST'])
@basic_auth.required
def add_compra():
    try:
        _json = request.get_json(force = True)        
        _data = _json['data']
        _idCliente = _json['idCliente']
        _idCurso = _json['idCurso']

        if _data and _idCliente and _idCurso and request.method == 'POST':
            sqlQuery = "INSERT INTO db_vendas.tbl_cliente_compra_cursos (data, idCliente, idCurso ) VALUES (%s,%s,%s)"
            bindData = (_data, _idCliente, _idCurso)
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)         
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify('Compra adicionado com sucesso!')
            response.status_code = 200
            return response
        else:
            return not_found()
    except Exception as error:
        return error, 500
    finally:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.close()
        conn.close()


#Criando as Rotas API para relação JOIN Cliente, Compra e Produtos/Cursos
#Buscando todos os endereços cadastrados (GET)
@app.route('/cliente/compras', methods = ['GET'])
@basic_auth.required
def compras():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute ('SELECT idCompra, data, idCliente, idCurso FROM db_vendas.tbl_cliente_compra_cursos')
        
        #cursor.execute("SELECT db_produtos.tbl_cursos.nome as Nome_do_Curso, db_produtos.tbl_cursos.preco as Preco_do_Curso, db_clientes.tbl_clientes.nome as Nome_do_Cliente, db_clientes.tbl_clientes.cpf FROM db_clientes.tbl_clientes INNER JOIN db_vendas.tbl_cliente_compra_cursos ON db_clientes.tbl_clientes.id = db_vendas.tbl_cliente_compra_cursos.idCliente INNER JOIN db_produtos.tbl_cursos ON db_produtos.tbl_cursos.idCurso = db_vendas.tbl_cliente_compra_cursos.idCurso")
        empRows = cursor.fetchall()
        respone = jsonify(empRows)
        respone.status_code = 200
        return respone
    except Exception as error:
        return jsonify({"error":f"{error}"}), 500
    finally:
        cursor.close()
        conn.close()



# http://127.0.0.1:5000/clientes/compras/id
@app.route('/cliente/compras/<int:idCliente>', methods = ['GET'])
@basic_auth.required
def id_compras (idCliente):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute ("SELECT db_produtos.tbl_cursos.nome as Nome_do_Curso, db_produtos.tbl_cursos.preco as Preco_do_Curso, db_clientes.tbl_clientes.nome as Nome_do_Cliente, db_clientes.tbl_clientes.cpf FROM db_clientes.tbl_clientes INNER JOIN db_vendas.tbl_cliente_compra_cursos ON db_clientes.tbl_clientes.id = db_vendas.tbl_cliente_compra_cursos.idCliente INNER JOIN db_produtos.tbl_cursos ON db_produtos.tbl_cursos.idCurso = db_vendas.tbl_cliente_compra_cursos.idCurso WHERE db_vendas.tbl_cliente_compra_cursos.idCliente = %s", idCliente)
        userRow = cursor.fetchall()
        if not userRow:
            return Response('Compra não cadastrada', status=404)
        response = jsonify(userRow)     
        response.status_code = 200
        return response
    except Exception as error:
        return jsonify({"error":f"{error}"}), 500
    finally:
        cursor.close() 
        conn.close()

# Alterando algum curso (PUT)
# No put, precisa passar o ID na rota, mas no próprio body eu posso manter o mesmo, ou colocar o número novo a ser alterado.
@app.route('/cliente/compras/<int:id>', methods=['PUT'])
@basic_auth.required
def update_curso(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        _json = request.get_json(force = True)
        _idCompra = _json['idCompra']
        _data = _json['data']
        _idCliente = _json['idCliente']
        _idCurso = _json['idCurso']

        if  _data and _idCliente and _idCurso and _idCompra and request.method == 'PUT':
            sqlQuery = "SELECT * FROM db_vendas.tbl_cliente_compra_cursos WHERE idCompra=%s"
            cursor.execute(sqlQuery, id)
            select = cursor.fetchone()
            if not select:
                return Response('Compra não cadastrada', status=400)
            sqlQuery = "UPDATE db_vendas.tbl_cliente_compra_cursos SET data=%s, idCliente=%s, idCurso=%s, idCompra=%s WHERE idCompra=%s"
            bindData = (_data, _idCliente, _idCurso, _idCompra, id)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify('Dados alterados com sucesso!')
            response.status_code = 200
            return response
        else:
            return not_found()
    except Exception as error:
        return jsonify({"error":f"{error}"}), 500
    finally:
        cursor.close()
        conn.close()


# Deletando algum curso (DELETE)
@app.route('/cliente/compras/<int:idCompra>', methods=['DELETE'])
@basic_auth.required
def delete_curso(idCompra):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sqlQuery = "SELECT * FROM db_vendas.tbl_cliente_compra_cursos WHERE idCompra=%s"
        cursor.execute(sqlQuery, idCompra)
        select = cursor.fetchone()
        if not select:
            return Response('Compra não cadastrada', status=400)
        cursor.execute("DELETE FROM db_vendas.tbl_cliente_compra_cursos WHERE idCompra =%s", (idCompra))
        conn.commit()
        respone = jsonify('Compra deletada com sucesso!')
        respone.status_code = 200
        return respone
    except Exception as error:
        return jsonify({"error":f"{error}"}), 500
    finally:
        cursor.close()
        conn.close()


@app.errorhandler(404)
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