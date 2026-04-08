from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)


DATABASE_URL = os.environ.get("postgresql://examen_db_nrgn_user:eMTLN7VcgZAxVr8M4qIVnBwLh7v61C8u@dpg-d7b7vu4hg0os73ab7qb0-a.virginia-postgres.render.com/examen_db_nrgn")

conn = psycopg2.connect(DATABASE_URL)

# crear tabla automáticamente
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