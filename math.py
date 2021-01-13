#!/usr/bin/python3
from flask import Flask, request

app = Flask(__name__)

def mesaj(text):
    return f"<h1>{text}</h1>"

@app.route("/<islem>/<bir>/<iki>")
def data(islem,bir,iki):
    assert islem == request.view_args['islem']
    assert bir == request.view_args["bir"]
    assert iki == request.view_args["iki"]
    if islem != "add" and islem != "sub" and islem != "div" and islem != "mul":
        return mesaj("Hatali islem")
    try:
        bir = int(bir)
        iki = int(iki)
        assert bir < 1000 and iki < 1000
    except:
        return mesaj("Arguments must be integer and less than 1000")
    #return mesaj(f"secilen islem: {islem} and bir: {bir} and iki: {iki} ")
    sembol = ""
    sonuc = 0
    if islem == "add":
        sembol = "+"
        sonuc = bir+iki
    elif islem == "sub":
        sembol = "-"
        sonuc = bir-iki
    elif islem == "div":
        sembol = "/"
        sonuc = bir / iki
    elif islem == "mul":
        sembol = "*"
        sonuc = bir * iki
    return mesaj(f"{bir}{sembol}{iki}={sonuc}")


@app.route("/<islem>/<bir>")
def fiki(islem,bir):
    assert islem == request.view_args['islem']
    assert bir == request.view_args["bir"]
    return mesaj("[!] Invalid usage. Try: /add-sub-div-mul/1/5")

@app.route("/<islem>")
def fbir(islem):
    assert islem == request.view_args['islem']
    return mesaj("[!] Invalid usage. Try: /add-sub-div-mul/1/5")


if __name__ == '__main__':
   app.run(host="0.0.0.0",port=8000)
