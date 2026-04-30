from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

produtos = [
    {"id":1, "nome":"Ração Cães", "preco":89.90},
    {"id":2, "nome":"Ração Gatos", "preco":79.90},
    {"id":3, "nome":"Brinquedo", "preco":29.90}
]

carrinho = []

@app.route('/')
def home():
    return render_template('index.html', produtos=produtos)

@app.route('/add', methods=['POST'])
def add():
    data = request.json
    carrinho.append(data)
    return jsonify({'total': len(carrinho)})

@app.route('/carrinho')
def carrinho_page():
    total = sum(p['preco']*p['qtd'] for p in carrinho)
    return render_template('carrinho.html', carrinho=carrinho, total=total)

if __name__ == '__main__':
    app.run(debug=True)