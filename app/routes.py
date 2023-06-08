from app import app, lst, sessions
from app.util import *
from flask import (
    render_template, 
    request, 
    url_for,
    redirect, 
    flash
)
from Rdb import BD

db = BD()


@app.route("/")
@app.route("/login", methods=["POST"])
def login():
    global sessions,lst
    if request.method == "POST":
        #try:
            email = request.form["email"]
            password = request.form["senha"]
            token = request.form["token"]
            if db.verify("email", email):
                print("boa")
            if token in lst:
                 o,c = gerar_tempo()
                 sessions[token] = {
                     "name": "Ricardo Cayoca",
                     "email": "ricardokayoca@gmail.com",
                     "open": o,
                     "close": c,
                     "token": token,
                     "convidados": 7,
                     "pontos": 6
                 }
                 return redirect(f"/home/{token}")
            return "erro sbhshs"
        #except:
            #return "Request inválido"
    
    token = generate_token(lst)
    lst.append(token)
    return render_template("login.html", token=token)


bd = BD("home.json")
@app.route("/home/<token>")
def home(token):
    if token not in lst:
        return redirect("/")
    info = sessions[str(token)]
    if close(info): return redirect("/")
    dados = bd.read()
    return render_template("home.html", cu=dados, dados=info)

@app.route("/perfil/<token>")
def perfil(token):
    if token not in lst:
        return redirect("/")
    info = sessions[str(token)]
    if close(info): return redirect("/")
    #return str(info)
    return render_template("perfil.html",info=info)

@app.route("/video/play/<token>/<tema>/<id>")
def video_play(token, tema, id):
    if token not in lst:
        return redirect("/")
    info = sessions[str(token)]
    if close(info): return redirect("/")
    
    dados = bd.read()
    if tema in dados:
        for x in dados[tema]:
            if x["id"] == id:
                return render_template("video.html", dados=info, tema=tema, video=x["video"])
    
    return f""" 
        <h2>Video não disponível</h2>
        <a href='/home/{token}'>Voltar</a>
           """


