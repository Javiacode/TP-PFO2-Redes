"""Servidor API Flask - Sistema de Gestion de Tareas (PFO2 - Redes).

Endpoints:
    POST /registro : registra un usuario con contraseña hasheada en SQLite.
    POST /login    : verifica credenciales contra la base de datos.
    GET  /tareas   : devuelve un HTML de bienvenida.
"""

import sqlite3

from flask import Flask, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

DATABASE = "tareas.db"


def get_db():
    """Abre una conexion a la base de datos SQLite."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Crea la tabla de usuarios si no existe."""
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


@app.route("/registro", methods=["POST"])
def registro():
    """Registra un usuario nuevo.

    Espera un JSON: {"usuario": "nombre", "contraseña": "1234"}
    La contraseña NUNCA se guarda en texto plano: se almacena su hash.
    """
    datos = request.get_json()

    if not datos or "usuario" not in datos or "contraseña" not in datos:
        return jsonify({"error": "Faltan los campos 'usuario' y 'contraseña'"}), 400

    usuario = datos["usuario"]
    contraseña = datos["contraseña"]

    # generate_password_hash aplica scrypt con salt aleatorio.
    password_hash = generate_password_hash(contraseña)

    try:
        conn = get_db()
        # Los ? son parametros: sqlite3 escapa los valores y evita inyeccion SQL.
        conn.execute(
            "INSERT INTO usuarios (usuario, password_hash) VALUES (?, ?)",
            (usuario, password_hash),
        )
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        # La columna usuario es UNIQUE: si ya existe, SQLite lanza este error.
        return jsonify({"error": "El usuario ya existe"}), 409

    return jsonify({"mensaje": f"Usuario '{usuario}' registrado correctamente"}), 201


@app.route("/login", methods=["POST"])
def login():
    """Verifica las credenciales del usuario.

    Espera un JSON: {"usuario": "nombre", "contraseña": "1234"}
    Compara el hash almacenado con el hash de la contraseña recibida.
    """
    datos = request.get_json()

    if not datos or "usuario" not in datos or "contraseña" not in datos:
        return jsonify({"error": "Faltan los campos 'usuario' y 'contraseña'"}), 400

    conn = get_db()
    fila = conn.execute(
        "SELECT password_hash FROM usuarios WHERE usuario = ?",
        (datos["usuario"],),
    ).fetchone()
    conn.close()

    # Se devuelve el mismo mensaje si el usuario no existe o si la
    # contraseña es incorrecta, para no revelar informacion al atacante.
    if fila is None or not check_password_hash(fila["password_hash"], datos["contraseña"]):
        return jsonify({"error": "Credenciales invalidas"}), 401

    return jsonify({"mensaje": f"Bienvenido, {datos['usuario']}!"}), 200


@app.route("/tareas", methods=["GET"])
def tareas():
    """Muestra una pagina HTML de bienvenida."""
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="utf-8">
        <title>Sistema de Gestion de Tareas</title>
    </head>
    <body>
        <h1>Bienvenido al Sistema de Gestion de Tareas</h1>
        <p>Has accedido correctamente al area de tareas.</p>
    </body>
    </html>
    """


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
