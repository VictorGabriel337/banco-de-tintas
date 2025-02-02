from flask import Flask, request, jsonify, redirect, url_for
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)

# Configuração do banco de dados
db_config = {
    'host': '127.0.0.1',         # endereço do servidor MySQL
    'user': 'BDteste',       # usuário do banco de dados
    'password': '461663',     # senha do banco de dados
    'database': 'dbteste',  # nome do banco de dados
    'port': '3306',  # Substitua por outra porta se necessário
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/cadastrar', methods=['POST'])
def cadastrar_usuario():
    usuario = request.form.get('usuario')
    email = request.form.get('email')
    telefone = request.form.get('telefone')
    endereco = request.form.get('endereco')
    cidade = request.form.get('cidade')
    senha = request.form.get('senha')
    repetir_senha = request.form.get('repetirsenha')



    # if not all([usuario, email, telefone, endereco, cidade, senha]):
    #      return jsonify({"error": "Todos os campos são obrigatórios!"}), 400

    if senha != repetir_senha:
        return jsonify({"error": "As senhas não correspondem"}), 400
    

      # Imprimir para depuração
    print(f"Usuário: {usuario}, Email: {email}, Telefone: {telefone}, Endereço: {endereco}, Cidade: {cidade}, Senha: {senha}")

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO usuarios (usuario, email, telefone, endereco, cidade, senha)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (usuario, email, telefone, endereco, cidade, senha))
        conn.commit()
        return redirect(url_for('success'))
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400
    
        

    finally:
        cursor.close()
        conn.close()

@app.route('/success')
def success():
    return "Cadastro realizado com sucesso!"

if __name__ == '__main__':
    app.run(debug=True)

