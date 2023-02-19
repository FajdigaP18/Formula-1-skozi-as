from bottle import *
import model


# glavni_model = model.Model()
dirkaci_model = model.Dirkac()
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

    return template("template/glavna.html")

@get("/dirkaci")
def dirkaci_stran():
    "Podatki pridobljeni iz modelov"

    # podatki = dirkaci_model.()

    return template("template/dirkaci.html")

@get("/dirkalisca")
def dirkalisca_stran():
    return template("template/dirkalisca.html")

@get("/ekipa")
def ekipa_stran():

    podatki = ekipa_model.pridobi_vse_ekipe()
    nemci = ekipa_model.pridobi_vse_nemce()
    anglezi = ekipa_model.pridobi_vse_angleze()
    italjani = ekipa_model.pridobi_vse_italijane()

    return template("template/ekipa.html", ekipe=podatki, nemci=nemci, anglezi=anglezi, italjani=italjani)


run(debug=True, reloader=True)


