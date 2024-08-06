from flask import Flask, redirect, url_for
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote

app = Flask(__name__)

user = 'root'
password = '@Lucia25037795'
host = 'localhost'
port = '3306'
database = 'trocafacil'
escaped_password = quote(password)
uri = f'mysql+pymysql://{user}:{escaped_password}@{host}:{port}/{database}'

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    nome = db.Column('nome', db.String(150))
    email = db.Column('email', db.String(50))
    password = db.Column('password', db.String(10))
    telefone = db.Column('telefone', db.String(50))
    endereco = db.Column('endereco', db.String(100))

    def __init__(self, nome, email, password, telefone, endereco):
        self.nome = nome
        self.email = email
        self.password = password
        self.telefone = telefone
        self.endereco = endereco


class Categoria(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    nome = db.Column('nome', db.String(100))

    def __init__(self, nome):
        self.nome = nome


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/cadastro/usuario")
def rota_usuario():
    return render_template('usuario.html', usuarios = Usuario.query.all(), titulo = "Usuário")

@app.route("/usuario/cadastrar", methods=['POST'])
def cadastrar_usuario():
    usuario = Usuario(request.form.get('nome'), request.form.get('email'), request.form.get('password'), request.form.get('telefone'), request.form.get('endereco'))
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('rota_usuario'))

@app.route("/usuario/detalhar/<int:id>")
def buscar_usuario(id):
    usuario = Usuario.query.get(id)
    return usuario.nome

@app.route("/usuario/editar/<int:id>", methods=['GET', 'POST'])
def editar_usuario(id):
    usuario = Usuario.query.get(id)
    if request.method == 'POST':
        usuario.nome = request.form.get('nome')
        usuario.email = request.form.get('email')
        usuario.password = request.form.get('password')
        usuario.telefone = request.form.get('telefone')
        usuario.endereco = request.form.get('endereco')
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('rota_usuario'))

    return render_template('editar_usuario.html', usuario = usuario, titulo = "Usuário")

@app.route("/usuario/remover/<int:id>")
def remover_usuario(id):
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('rota_usuario'))


@app.route("/cadastro/anuncio")
def anuncio():
    return render_template('anuncio.html', categorias = Categoria.query.all(), titulo = "Anúncio")

@app.route("/anuncio/cadastrar", methods=['POST'])
def cadastrar_anuncio():
    return request.form

@app.route("/anuncios/pergunta")
def pergunta_anuncio():
    return render_template('pergunta.html', titulo = "Perguntas do Anúncio")

@app.route("/anuncios/compra")
def compra_anuncio():
    print('Compra realizada com sucesso!')
    return ""

@app.route("/anuncios/favoritos")
def anuncio_favorito():
    print('Anúncio favoritado com sucesso!')
    return ""

@app.route("/config/categoria")
def rota_categoria():
    return render_template('categoria.html', categorias = Categoria.query.all(), titulo = "Categoria")

@app.route("/categoria/cadastrar", methods=['POST'])
def cadastrar_categoria():
    categoria = Categoria(request.form.get('nome'))
    db.session.add(categoria)
    db.session.commit()
    return redirect(url_for('rota_categoria'))

@app.route("/relatorio/vendas")
def relatorio_venda():
    return render_template('vendas.html', titulo = "Relatório de Vendas")

@app.route("/relatorio/compras")
def relatorio_compra():
    return render_template('compras.html', titulo = "Relatório de Compras")


if __name__ == 'main':
    with app.app_context():
        print('trocafacil')
        db.create_all()