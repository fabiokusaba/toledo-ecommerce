from flask import Flask, make_response
from markupsafe import escape
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/sobre")
def sobre():
    return "<h1> Tudo o que você procura está aqui, venda, compre, desapegue!</h1>"

@app.route("/sobre/privacidade")
def sobre_privacidade():
    return "<h4> Nosso site segue as Leis Gerais de Proteção aos Dados, seus dados estão totalmente seguros.</h4>"

@app.route("/user/<username>")
def username(username):
    cookie = make_response("<h2>cookie criado</h2>")
    cookie.set_cookie('username', username)
    return cookie

@app.route("/user2/")
@app.route("/user2/<username>")
def username2(username=None):
    cookie_username = request.cookies.get('username')
    return render_template('user.html', username=username, cookie_username=cookie_username)
