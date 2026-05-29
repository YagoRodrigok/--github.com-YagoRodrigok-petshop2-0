from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Lista para armazenar pets cadastrados
pets = []

@app.route('/')
def index():
    return render_template('index.html', pets=pets)

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form['nome']
        especie = request.form['especie']
        dono = request.form['dono']
        servico = request.form['servico']
        horario = request.form['horario']
        pets.append({'nome': nome, 'especie': especie, 'dono': dono, 'servico': servico, 'horario': horario})
        return redirect(url_for('index'))
    return render_template('cadastrar.html')

@app.route('/detalhes/<int:pet_id>')
def detalhes(pet_id):
    if 0 <= pet_id < len(pets):
        pet = pets[pet_id]
        return render_template('detalhes.html', pet=pet, pet_id=pet_id)
    return redirect(url_for('index'))

@app.route('/editar/<int:pet_id>', methods=['GET', 'POST'])
def editar(pet_id):
    if 0 <= pet_id < len(pets):
        pet = pets[pet_id]
        if request.method == 'POST':
            pet['nome'] = request.form['nome']
            pet['especie'] = request.form['especie']
            pet['dono'] = request.form['dono']
            pet['servico'] = request.form['servico']
            pet['horario'] = request.form['horario']
            return redirect(url_for('detalhes', pet_id=pet_id))
        return render_template('editar.html', pet=pet)
    return redirect(url_for('index'))

@app.route('/remover/<int:pet_id>', methods=['POST'])
def remover(pet_id):
    if 0 <= pet_id < len(pets):
        pets.pop(pet_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)