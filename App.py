from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# initializations
app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'crudpython'
mysql = MySQL(app)

# settings
app.secret_key = "mysecretkey"

# routes
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', usuarios = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        nombre = request.form['nombre']
        celular = request.form['celular']
        correo = request.form['correo']
        apellidos = request.form['apellidos']
        passd = request.form['passd']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios (nombre, apellidos, celular, correo, passd) VALUES (%s,%s,%s,%s,%s)", (nombre, apellidos, celular, correo, passd))
        mysql.connection.commit()
        flash('Contacto Creado con éxito')
        return redirect(url_for('Index'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        celular = request.form['celular']
        correo = request.form['correo']
        apellidos = request.form['apellidos']
        passd = request.form['passd']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE usuarios
            SET nombre = %s,
                correo = %s,
                celular = %s,
                apellidos = %s,
                passd = %s
            WHERE id = %s
        """, (nombre, correo, celular, apellidos, passd, id))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM usuarios WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contacto eliminado con éxito')
    return redirect(url_for('Index'))

# starting the app
if __name__ == "__main__":
    app.run(port=3010, debug=True)
