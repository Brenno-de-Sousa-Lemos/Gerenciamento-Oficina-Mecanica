from models.database.connection_db import get_connection
from flask import Flask, render_template, request, redirect, flash
from flask import session
import hashlib

app = Flask(__name__)
app.secret_key = "secretkey"

def criptografar_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

@app.route("/")
def index():
    return redirect("/login")

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

    return render_template("login.html")

def criar_tabela_usuario():
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

criar_tabela_usuario()

from models.database.connection_db import get_connection

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

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nome = request.form["nome"]
        senha = request.form["senha"]

        if not nome:
            flash("Preencha todos os campos!")
            return redirect("/login")
        
        if not senha:
            flash("Preencha todos os campos!")
            return redirect("/login")
        if nome and senha:
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
    return render_template("home/home.html")

@app.route("/usuarios")
def visualizar_usuarios():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()

    conn.close()

    return render_template("usuarios.html", usuarios=usuarios)

@app.route("/criar_ordem_nova", methods=["GET", "POST"])
def ordem():
    if request.method == "POST":
        cliente = request.form.get("cliente")
        descricao = request.form.get("descricao")

        if not cliente:
            flash("Falta o nome do cliente!", "erro_cliente")
            return redirect("/criar_ordem_nova")

        if not descricao:
            flash("Falta a descrição do problema!", "erro_descricao")
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

    return render_template("cadastro/cadastro_ordens_servico.html")

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