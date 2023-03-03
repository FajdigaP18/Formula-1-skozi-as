from bottle import *
import model


# glavni_modeli
dirkaci_model = model.Dirkac()
dirkalisca_model = model.Dirkalisce()
ekipa_model = model.Ekipa()

# koliko zadetkov na stran
page_size = 100

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

    page_number = int(request.query.get('page', '1'))
    offset = (page_number - 1) * page_size
    limit = page_size

    total_pages = (855 + page_size - 1) // page_size

    podatki = dirkaci_model.vsi_dirkaci(limit, offset)

    return template("template/dirkaci.html", dirkaci=podatki,  total_pages=total_pages, current_page=page_number)

@get("/dirkaci/<did:int>")
def dirkaci_detajli(did):

    dirkac = dirkaci_model.dobi_dirkaca(did)
    vse_ekipe = dirkaci_model.vse_ekipe(did)
    najbol_uvrstitve = dirkaci_model.najboljse_uvrstitve(dirkac.ime, dirkac.priimek)
    zmag_oder = dirkaci_model.zmagovalni_oder(did) 
    datum = dirkaci_model.dobi_dirkaca(did).rojstvo
    drzav = dirkaci_model.dobi_dirkaca(did).drzava

    return template("template/dirkac_detaili.html", dirkac=dirkac, ekipe=vse_ekipe, uvrstitve=najbol_uvrstitve, oder=zmag_oder, d=datum, drzavljanstvo=drzav)

@get("/dirkalisca")
def dirkalisca_stran():

    dirkalisca = dirkalisca_model.pridobi_vsa_dirkalisca()

    return template("template/dirkalisca.html", dirkalisca=dirkalisca)

@get("/dirkalisca/<did:int>")
def dirkalisca_detajli(did):
    dirkalisce = dirkalisca_model.pridobi_dirkalisce(did)
    dirkac = dirkalisca_model.pridobi_vsa_dirkalisca()
    kdo = dirkalisca_model.kdo_najveckrat_zmagal(did)
    return template("template/dirkalisce_detaili.html", dirkac=dirkac, kdo = kdo, dirkalisce=dirkalisce)

@get("/ekipa")
def ekipa_stran():
    podatki = ekipa_model.pridobi_vse_ekipe()
    nemci = ekipa_model.pridobi_vse_nemce()
    anglezi = ekipa_model.pridobi_vse_angleze()
    italjani = ekipa_model.pridobi_vse_italijane()

    return template("template/ekipa.html", ekipe=podatki, nemci=nemci, anglezi=anglezi, italjani=italjani)

@get("/ekipa/<eid:int>")
def ekipe_detajli(eid):
    ekipa = ekipa_model.pridobi_ekipo(eid)
    dirkaci = ekipa_model.ekipa_vsi_dirkaci(eid)
    sezone = ekipa_model.ekipa_sezone(eid)
    return template("template/ekipa_detaili.html", ekipa=ekipa, dirkaci=dirkaci, sezone=sezone)

@get("/search/<query>")
def iskanje(query):
    
    ekipe = ekipa_model.poisci_po_imenu(query, limit=10)

    return template("template/search.html", ekipe=ekipe)


run(debug=True, reloader=True)


