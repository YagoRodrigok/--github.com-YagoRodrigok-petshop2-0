from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime, date
import json

app = Flask(__name__)
flask_cors.CORS(app)

# Inicializar banco de dados
def init_db():
    conn = sqlite3.connect('petshop.db')
    cursor = conn.cursor()
    
    # Tabela clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT,
            telefone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabela pets
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            nome TEXT NOT NULL,
            especie TEXT NOT NULL,
            raca TEXT,
            idade INTEGER,
            peso REAL,
            FOREIGN KEY (cliente_id) REFERENCES clientes (id)
        )
    ''')
    
    # Tabela agendamentos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agendamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            pet_id INTEGER,
            servico TEXT NOT NULL,
            data DATE NOT NULL,
            hora TEXT NOT NULL,
            observacoes TEXT,
            status TEXT DEFAULT 'confirmado',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (cliente_id) REFERENCES clientes (id),
            FOREIGN KEY (pet_id) REFERENCES pets (id)
        )
    ''')
    
    # Inserir dados de exemplo
    cursor.execute("SELECT COUNT(*) FROM clientes")
    if cursor.fetchone()[0] == 0:
        clientes_exemplo = [
            ('João Silva', 'joao@email.com', '(11) 99999-1111'),
            ('Maria Santos', 'maria@email.com', '(11) 99999-2222'),
            ('Pedro Oliveira', 'pedro@email.com', '(11) 99999-3333'),
        ]
        cursor.executemany("INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)", clientes_exemplo)
        
        pets_exemplo = [
            (1, 'Rex', 'Cão', 'Vira-lata', 5, 15.5),
            (1, 'Luna', 'Gato', 'Siames', 3, 4.2),
            (2, 'Max', 'Cão', 'Golden Retriever', 2, 25.0),
            (3, 'Mimi', 'Gato', 'Persa', 4, 5.1),
        ]
        cursor.executemany("INSERT INTO pets (cliente_id, nome, especie, raca, idade, peso) VALUES (?, ?, ?, ?, ?, ?)", pets_exemplo)
    
    conn.commit()
    conn.close()

# Rotas API
@app.route('/api/clientes')
def get_clientes():
    conn = sqlite3.connect('petshop.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM clientes ORDER BY nome")
    clientes = [{'id': row[0], 'nome': row[1]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(clientes)

@app.route('/api/pets/<int:cliente_id>')
def get_pets(cliente_id):
    conn = sqlite3.connect('petshop.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nome, especie, raca, idade, peso 
        FROM pets WHERE cliente_id = ? ORDER BY nome
    """, (cliente_id,))
    pets = []
    for row in cursor.fetchall():
        pets.append({
            'id': row[0], 'nome': row[1], 'especie': row[2], 
            'raca': row[3], 'idade': row[4], 'peso': row[5]
        })
    conn.close()
    return jsonify(pets)

@app.route('/api/agendamentos', methods=['GET', 'POST'])
def agendamentos():
    conn = sqlite3.connect('petshop.db')
    cursor = conn.cursor()
    
    if request.method == 'POST':
        data = request.json
        try:
            cursor.execute("""
                INSERT INTO agendamentos (cliente_id, pet_id, servico, data, hora, observacoes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (data['cliente_id'], data['pet_id'], data['servico'], 
                  data['data'], data['hora'], data['observacoes']))
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'agendamento': {
                'id': cursor.lastrowid, 'servico': data['servico'],
                'data': data['data'], 'hora': data['hora']
            }})
        except Exception as e:
            conn.close()
            return jsonify({'success': False, 'error': str(e)})
    
    # GET - listar agendamentos
    cursor.execute("""
        SELECT a.id, a.servico, a.data, a.hora, a.observacoes, a.status,
               c.nome as cliente_nome, p.nome as pet_nome
        FROM agendamentos a
        JOIN clientes c ON a.cliente_id = c.id
        JOIN pets p ON a.pet_id = p.id
        ORDER BY a.data, a.hora
    """)
    agendamentos = []
    for row in cursor.fetchall():
        agendamentos.append({
            'id': row[0], 'servico': row[1], 'data': row[2],
            'hora': row[3], 'observacoes': row[4], 'status': row[5],
            'cliente_nome': row[6], 'pet_nome': row[7]
        })
    conn.close()
    return jsonify(agendamentos)

# Rota para servir arquivos estáticos
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agendamento.html')
def agendamento():
    return render_template('agendamento.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)