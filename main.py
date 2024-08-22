from flask import Flask, redirect, url_for
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import (current_user, LoginManager, login_user, logout_user, login_required)
import hashlib

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

app.secret_key = 'cavalo come gohan no cafe da manha'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Usuario(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    nome = db.Column('nome', db.String(150))
    email = db.Column('email', db.String(50))
    password = db.Column('password', db.String(255))
    telefone = db.Column('telefone', db.String(50))
    endereco = db.Column('endereco', db.String(100))

    def __init__(self, nome, email, password, telefone, endereco):
        self.nome = nome
        self.email = email
        self.password = password
        self.telefone = telefone
        self.endereco = endereco

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)


class Anuncio(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    titulo = db.Column('titulo', db.String(150))
    descricao = db.Column('descricao', db.String(150))
    quantidade = db.Column('quantidade', db.Integer)
    preco = db.Column('preco', db.Numeric(10, 2))
    categoria_id = db.Column('categoria_id', db.Integer, db.ForeignKey("categoria.id"))
    usuario_id = db.Column('usuario_id', db.Integer, db.ForeignKey("usuario.id"))

    def __init__(self, titulo, descricao, quantidade, preco, categoria_id, usuario_id):
        self.titulo = titulo
        self.descricao = descricao
        self.quantidade = quantidade
        self.preco = preco
        self.categoria_id = categoria_id
        self.usuario_id = usuario_id


class Categoria(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    nome = db.Column('nome', db.String(100))

    def __init__(self, nome):
        self.nome = nome


class Compra(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    anuncio_id = db.Column('anuncio_id', db.Integer, db.ForeignKey("anuncio.id"))
    usuario_id = db.Column('usuario_id', db.Integer, db.ForeignKey("usuario.id"))

    def __init__(self, anuncio_id, usuario_id):
        self.anuncio_id = anuncio_id
        self.usuario_id = usuario_id


class Favorito(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    anuncio_id = db.Column('anuncio_id', db.Integer, db.ForeignKey("anuncio.id"))
    usuario_id = db.Column('usuario_id', db.Integer, db.ForeignKey("usuario.id"))

    def __init__(self, anuncio_id, usuario_id):
        self.anuncio_id = anuncio_id
        self.usuario_id = usuario_id


class Pergunta(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    texto = db.Column('texto', db.String(150))
    anuncio_id = db.Column('anuncio_id', db.Integer, db.ForeignKey("anuncio.id"))
    usuario_id = db.Column('usuario_id', db.Integer, db.ForeignKey("usuario.id"))

    def __init__(self, texto, anuncio_id, usuario_id):
        self.texto = texto
        self.anuncio_id = anuncio_id
        self.usuario_id = usuario_id


class Resposta(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    texto = db.Column('texto', db.String(150))
    pergunta_id = db.Column('pergunta_id', db.Integer, db.ForeignKey("pergunta.id"))
    usuario_id = db.Column('usuario_id', db.Integer, db.ForeignKey("usuario.id"))

    def __init__(self, texto, pergunta_id, usuario_id):
        self.texto = texto
        self.pergunta_id = pergunta_id
        self.usuario_id = usuario_id



@app.errorhandler(404)
def pagina_nao_encontrada(error):
    return render_template('error404.html')


@app.errorhandler(500)
def erro_interno_servidor(error):
    return render_template('error500.html')


@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(id)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = hashlib.sha512(str(request.form.get('password')).encode("utf-8")).hexdigest()

        user = Usuario.query.filter_by(email=email, password=password).first()

        if user:
            login_user(user)
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
        
    return render_template('login.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/cadastro/usuario")
def rota_usuario():
    return render_template('usuario.html', usuarios = Usuario.query.all(), titulo = "Usuário")

@app.route("/usuario/cadastrar", methods=['POST'])
def cadastrar_usuario():
    hash_password = hashlib.sha512(str(request.form.get('password')).encode("utf-8")).hexdigest()
    usuario = Usuario(request.form.get('nome'), request.form.get('email'), hash_password, request.form.get('telefone'), request.form.get('endereco'))
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('rota_usuario'))

@app.route("/usuario/detalhar/<int:id>")
@login_required
def buscar_usuario(id):
    usuario = Usuario.query.get(id)
    return render_template('detalhar_usuario.html', usuario = usuario, titulo = "Usuário")

@app.route("/usuario/editar/<int:id>", methods=['GET', 'POST'])
@login_required
def editar_usuario(id):
    usuario = Usuario.query.get(id)
    if request.method == 'POST':
        usuario.nome = request.form.get('nome')
        usuario.email = request.form.get('email')
        usuario.password = hashlib.sha512(str(request.form.get('password')).encode("utf-8")).hexdigest()
        usuario.telefone = request.form.get('telefone')
        usuario.endereco = request.form.get('endereco')
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('rota_usuario'))

    return render_template('editar_usuario.html', usuario = usuario, titulo = "Usuário")

@app.route("/usuario/remover/<int:id>")
@login_required
def remover_usuario(id):
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('rota_usuario'))


@app.route("/cadastro/anuncio")
@login_required
def rota_anuncio():
    return render_template('anuncio.html', categorias = Categoria.query.all(), anuncios = Anuncio.query.all(), titulo = "Anúncio")

@app.route("/anuncio/cadastrar", methods=['POST'])
@login_required
def cadastrar_anuncio():
    user_id = current_user.id
    anuncio = Anuncio(request.form.get('titulo'), request.form.get('descricao'), request.form.get('quantidade'), request.form.get('preco'), request.form.get('categoria'), user_id)
    db.session.add(anuncio)
    db.session.commit()
    return redirect(url_for('rota_anuncio'))

@app.route("/anuncio/detalhar/<int:id>")
@login_required
def buscar_anuncio(id):
    anuncio = Anuncio.query.get(id)
    return render_template('detalhar_anuncio.html', anuncio = anuncio, titulo = "Anúncio")

@app.route("/anuncio/editar/<int:id>", methods=['GET', 'POST'])
@login_required
def editar_anuncio(id):
    anuncio = Anuncio.query.get(id)
    if request.method == 'POST':
        anuncio.titulo = request.form.get('titulo')
        anuncio.descricao = request.form.get('descricao')
        anuncio.quantidade = request.form.get('quantidade')
        anuncio.preco = request.form.get('preco')
        anuncio.categoria_id = request.form.get('categoria')
        anuncio.usuario_id = request.form.get('usuario')
        db.session.add(anuncio)
        db.session.commit()
        return redirect(url_for('rota_anuncio'))

    return render_template('editar_anuncio.html', anuncio = anuncio, categorias = Categoria.query.all(), titulo = "Anúncio")

@app.route("/anuncio/remover/<int:id>")
@login_required
def remover_anuncio(id):
    anuncio = Anuncio.query.get(id)
    db.session.delete(anuncio)
    db.session.commit()
    return redirect(url_for('rota_anuncio'))

@app.route("/anuncio/comprar/<int:id>")
@login_required
def comprar_anuncio(id):
    user_id = current_user.id
    compra = Compra(id, user_id)
    db.session.add(compra)
    db.session.commit()
    return redirect(url_for('rota_anuncio'))

@app.route("/anuncio/favoritar/<int:id>")
@login_required
def favoritar_anuncio(id):
    user_id = current_user.id
    favorito = Favorito(id, user_id)
    db.session.add(favorito)
    db.session.commit()
    return redirect(url_for('rota_anuncio'))


@app.route("/anuncios/pergunta")
@login_required
def pergunta_anuncio():
    return render_template('pergunta.html', perguntas = Pergunta.query.all(), titulo = "Faça uma pergunta")


@app.route("/anuncios/pergunta/enviar", methods=['POST'])
@login_required
def enviar_pergunta():
    pergunta = Pergunta(request.form.get('texto'), request.form.get('anuncio_id'), request.form.get('usuario_id'))
    db.session.add(pergunta)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/anuncios/resposta/enviar", methods=['GET', 'POST'])
@login_required
def enviar_resposta():
    if request.method == 'POST':
        pergunta = Resposta(request.form.get('texto'), request.form.get('pergunta_id'), request.form.get('usuario_id'))
        db.session.add(pergunta)
        db.session.commit()
    return render_template('resposta.html', respostas = Resposta.query.all(), titulo = "Pense na resposta")


@app.route("/anuncios/compra")
@login_required
def compra_anuncio():
    return render_template('compras_realizadas.html', compras = Compra.query.all(), titulo = "Compras")


@app.route("/anuncios/favoritos")
@login_required
def anuncio_favorito():
    return render_template('anuncios_favoritos.html', favoritos = Favorito.query.all(), titulo = "Favoritos")


@app.route("/config/categoria")
@login_required
def rota_categoria():
    return render_template('categoria.html', categorias = Categoria.query.all(), titulo = "Categoria")

@app.route("/categoria/cadastrar", methods=['POST'])
@login_required
def cadastrar_categoria():
    categoria = Categoria(request.form.get('nome'))
    db.session.add(categoria)
    db.session.commit()
    return redirect(url_for('rota_categoria'))

@app.route("/categoria/detalhar/<int:id>")
@login_required
def buscar_categoria(id):
    categoria = Categoria.query.get(id)
    return render_template('detalhar_categoria.html', categoria = categoria, titulo = "Categoria")

@app.route("/categoria/editar/<int:id>", methods=['GET', 'POST'])
@login_required
def editar_categoria(id):
    categoria = Categoria.query.get(id)
    if request.method == 'POST':
        categoria.nome = request.form.get('nome')
        db.session.add(categoria)
        db.session.commit()
        return redirect(url_for('rota_categoria'))

    return render_template('editar_categoria.html', categoria = categoria, titulo = "Categoria")

@app.route("/categoria/remover/<int:id>")
@login_required
def remover_categoria(id):
    categoria = Categoria.query.get(id)
    db.session.delete(categoria)
    db.session.commit()
    return redirect(url_for('rota_categoria'))


@app.route("/relatorio/vendas")
@login_required
def relatorio_venda():
    return render_template('vendas.html', titulo = "Relatório de Vendas")


@app.route("/relatorio/compras")
@login_required
def relatorio_compra():
    return render_template('compras.html', titulo = "Relatório de Compras")


if __name__ == 'main':
    with app.app_context():
        print('trocafacil')
        db.create_all()