import flask
import json
from datetime import date

app = flask.Flask(__name__)
agendamentos = []  # Lista simples em memória

@app.route('/agendar', methods=['GET', 'POST'])
def agendar():
    if flask.request.method == 'POST':
        data = flask.request.json
        agendamentos.append(data)
        return flask.jsonify({'ok': True})
    
    hoje = date.today().isoformat()
    hoje_ags = [a for a in agendamentos if a['data'] == hoje]
    return flask.jsonify(hoje_ags)

if __name__ == '__main__':
    app.run(debug=True, port=5000)