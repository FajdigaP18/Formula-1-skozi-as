from bottle import *
import model


# glavni_model = model.Model()
dirkaci_model = model.Dirkac()
dirkalisca_model = model.Dirkalisce()
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

    podatki = dirkaci_model.vsi_dirkaci()

    return template("template/dirkaci.html", dirkaci=podatki)

@get("/dirkaci/<did:int>")
def dirkaci_detajli(did):

    dirkac = model.Dirkac.dobi_dirkaca(did)
    
    return template("template/dirkac_detaili.html", dirkac=dirkac)

@get("/dirkalisca")
def dirkalisca_stran():

    dirkalisca = dirkalisca_model.pridobi_vsa_dirkalisca()

    return template("template/dirkalisca.html", dirkalisca=dirkalisca)

@get("/dirkalisca/<did:int>")
def dirkalisca_detajli(did):

    dirkac = model.Dirkalisce.pridobi_vsa_dirkalisca()

    return template("template/dirkalisce_detaili.html", dirkac=dirkac)

@get("/ekipa")
def ekipa_stran():

    podatki = ekipa_model.pridobi_vse_ekipe()
    nemci = ekipa_model.pridobi_vse_nemce()
    anglezi = ekipa_model.pridobi_vse_angleze()
    italjani = ekipa_model.pridobi_vse_italijane()

    return template("template/ekipa.html", ekipe=podatki, nemci=nemci, anglezi=anglezi, italjani=italjani)


run(debug=True, reloader=True)


