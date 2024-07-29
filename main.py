from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1> Ecommerce FastBuy</h1>"

@app.route("/sobre")
def sobre():
    return "<h1> Tudo o que você procura está aqui, venda, compre, desapegue!</h1>"

@app.route("/sobre/privacidade")
def sobre_privacidade():
    return "<h4> Nosso site segue as Leis Gerais de Proteção aos Dados, seus dados estão totalmente seguros.</h4>"