from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/cadastro/usuario")
def usuario():
    return render_template('usuario.html', titulo="Cadastro de Usuário")

@app.route("/cadastro/cadastrar_usuario", methods=['POST'])
def cadastrar_usuario():
    return request.form

@app.route("/cadastro/anuncio")
def anuncio():
    return render_template('anuncio.html', titulo="Cadastro de Anúncio")

@app.route("/cadastro/cadastrar_anuncio", methods=['POST'])
def cadastrar_anuncio():
    return request.form

@app.route("/anuncios/pergunta")
def pergunta_anuncio():
    return render_template('pergunta.html', titulo="Perguntas do Anúncio")

@app.route("/anuncios/compra")
def compra_anuncio():
    print('Compra realizada com sucesso!')
    return ""

@app.route("/anuncios/favoritos")
def anuncio_favorito():
    print('Anúncio favoritado com sucesso!')
    return ""

@app.route("/config/categoria")
def categoria_config():
    return render_template('categoria.html', titulo="Configurações da Categoria")

@app.route("/relatorio/vendas")
def relatorio_venda():
    return render_template('vendas.html', titulo="Relatório de Vendas")

@app.route("/relatorio/compras")
def relatorio_compra():
    return render_template('compras.html', titulo="Relatório de Compras")