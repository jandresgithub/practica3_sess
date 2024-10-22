from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'unaclavesecreta'

def generar_id():
    if 'seminarios' in session and len(session['seminarios']) > 0:
        return max(item['id'] for item in session['seminarios']) + 1
    else:
        return 1

@app.route("/")
def index():
    if 'seminarios' not in session:
        session['seminarios'] = []
        
    seminarios = session.get('seminarios', [])
    return render_template('index.html', seminarios=seminarios)

@app.route("/nuevo", methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        fecha = request.form['fecha']
        turno = request.form['turno']
        seminario = request.form['seminario']

        nuevo_seminario = {
            'id': generar_id(),
            'nombre': nombre,
            'apellidos': apellidos,
            'fecha': fecha,
            'turno': turno,
            'seminario': seminario
        }
        
        if 'seminarios' not in session:
            session['seminarios'] = []

        session['seminarios'].append(nuevo_seminario)
        session.modified = True
        return redirect(url_for('index'))

    seminarios_disponibles = ['Inteligencia Artificial', 'Machine Learning', 'Simulación con Arena', 'Robótica Educativa']
    return render_template('nuevo.html', seminarios_disponibles=seminarios_disponibles)

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    lista_seminarios = session.get('seminarios', [])
    seminario = next((c for c in lista_seminarios if c['id'] == id), None)
    
    if not seminario:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        seminario['nombre'] = request.form['nombre']
        seminario['apellidos'] = request.form['apellidos']
        seminario['fecha'] = request.form['fecha']
        seminario['turno'] = request.form['turno']
        seminario['seminario'] = request.form['seminario']
        session.modified = True
        return redirect(url_for('index'))
    
    seminarios_disponibles = ['Inteligencia Artificial', 'Machine Learning', 'Simulación con Arena', 'Robótica Educativa']
    return render_template('editar.html', seminario=seminario, seminarios_disponibles=seminarios_disponibles)

@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    lista_seminarios = session.get('seminarios', [])
    seminario = next((c for c in lista_seminarios if c['id'] == id), None)
    
    if seminario:
        session['seminarios'].remove(seminario)
        session.modified = True
        
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
