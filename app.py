from flask import Flask, request, jsonify
import sqlite3
import json

app = Flask(__name__)

# Criar banco de dados simples
def init_db():
    conn = sqlite3.connect('petshop.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS agendamentos
                 (id INTEGER PRIMARY KEY, nome TEXT, pet TEXT, 
                  servico TEXT, data TEXT, hora TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return '''
    <h1>🐾 PetShop Cuidar</h1>
    <a href="/agendar">Agendar Serviço</a>
    '''

@app.route('/api/agendamentos', methods=['GET', 'POST'])
def agendamentos():
    conn = sqlite3.connect('petshop.db')
    c = conn.cursor()
    
    if request.method == 'POST':
        data = request.json
        c.execute("INSERT INTO agendamentos (nome, pet, servico, data, hora) VALUES (?, ?, ?, ?, ?)",
                  (data['nome'], data['pet'], data['servico'], data['data'], data['hora']))
        conn.commit()
        conn.close()
        return jsonify({'ok': True})
    
    c.execute("SELECT * FROM agendamentos ORDER BY data, hora")
    ags = [{'id':r[0], 'nome':r[1], 'pet':r[2], 'servico':r[3], 'data':r[4], 'hora':r[5]} 
           for r in c.fetchall()]
    conn.close()
    return jsonify(ags)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)