from flask import Flask, render_template, request, redirect
import psycopg2
import os

DATABASE_URL = os.environ.get("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)


cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS personas (
    id SERIAL PRIMARY KEY,
    dni VARCHAR(20) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    direccion TEXT,
    telefono VARCHAR(20)
);
""")
conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/guardar', methods=['POST'])
def guardar():
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO personas (dni, nombre, apellido, direccion, telefono) VALUES (%s,%s,%s,%s,%s)",
        (
            request.form['dni'],
            request.form['nombre'],
            request.form['apellido'],
            request.form['direccion'],
            request.form['telefono']
        )
    )
    conn.commit()
    return redirect('/')

@app.route('/administrar')
def administrar():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personas")
    personas = cursor.fetchall()
    return render_template('administrar.html', personas=personas)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM personas WHERE id=%s", (id,))
    conn.commit()
    return redirect('/administrar')

if __name__ == '__main__':
    app.run()