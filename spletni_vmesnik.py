from bottle import *
import model


glavni_model = model.Model()
ekipa_model = model.Ekipa()

@route("/static/img/<filename>")
def serve_static_files_img(filename):
    return static_file(
        filename, root="./static/img"
    )

@route("/static/css/<filename>")
def serve_static_files_css(filename):
    return static_file(
        filename, root="./static/css"
    )

@get("/")
def glavna_stran():

    podatki = glavni_model.dobi_vse_uporabnike()

    return template("template/glavna.html", uporabniki=podatki)

@get("/dirkaci")
def dirkaci_stran():
    "Podatki pridobljeni iz modelov"

    # podatki = 

    return template("template/dirkaci.html")

@get("/dirkalisca")
def dirkalisca_stran():
    return template("template/dirkalisca.html")

@get("/ekipa")
def ekipa_stran():

    podatki = ekipa_model.pridobi_vse_ekipe()

    return template("template/ekipa.html", ekipe=podatki)


run(debug=True, reloader=True)


