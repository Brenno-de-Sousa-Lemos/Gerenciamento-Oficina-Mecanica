from flask import Flask, render_template, request, redirect, flash
from flask import session
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = "segredo" 

def get_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def criptografar_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def criar_tabela():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            senha TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

criar_tabela()

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        senha = request.form["senha"]

        if not nome or not senha:
            flash("Preencha todos os campos!")
            return redirect("/cadastro")

        senha_criptografada = criptografar_senha(senha)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO usuarios (nome, senha)
            VALUES (?, ?)
        """, (nome, senha_criptografada))

        conn.commit()
        conn.close()

        flash("Cadastro realizado com sucesso!")
        return redirect("/login")

    return render_template("cadastro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nome = request.form["nome"]
        senha = request.form["senha"]

        if not nome or not senha:
            flash("Preencha todos os campos!")
            return redirect("/login")

        senha_criptografada = criptografar_senha(senha)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM usuarios
            WHERE nome = ? AND senha = ?
        """, (nome, senha_criptografada))

        usuario = cursor.fetchone()
        conn.close()

        if usuario:
            return redirect("/home")
        else:
            flash("Nome ou senha inválidos")
            return redirect("/login")

    return render_template("login.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/usuarios")
def visualizar_usuarios():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()

    conn.close()

    return render_template("usuarios.html", usuarios=usuarios)

def criar_tabela_ordens():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ordens_servico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT NOT NULL,
            descricao TEXT NOT NULL,
            data TEXT
        )
    """)

    conn.commit()
    conn.close()

criar_tabela_ordens()

@app.route("/criar_ordem_nova", methods=["GET", "POST"])
def ordem():
    if request.method == "POST":
        cliente = request.form.get("cliente")
        descricao = request.form.get("descricao")

        if not cliente or not descricao:
            flash("Preencha todos os campos!")
            return redirect("/criar_ordem_nova")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO ordens_servico (cliente, descricao)
            VALUES (?, ?)
        """, (cliente, descricao))

        conn.commit()
        conn.close()

        flash("Ordem cadastrada com sucesso!")
        return redirect("/ordens_servico")

    return render_template("cadastro_ordens_servico.html")

@app.route("/ordens_servico")
def listar_ordens():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM ordens_servico")
    ordens = cursor.fetchall()

    conn.close()

    return render_template("ordens_servico.html", ordens=ordens)

if __name__ == "__main__":
    app.run(debug=True)