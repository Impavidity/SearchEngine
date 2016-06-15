from engine import app
from flask import render_template, request, redirect, url_for

default_page_n = 10

@app.route('/',methods=["POST","GET"])
def index():
    if request.method == "GET":
        return render_template("home.html")
    if request.method == "POST":
        queryWords = request.form["iQuery"]
        return redirect(url_for("result",page=1))

@app.route('/result/<page>', methods=["GET","POST"])
def result(page):
    canditates = [1,5,6,9,10,11,12,13,14,18,19,22,23,24,27,29,30,36,37,38,40]
    npage = len(canditates)/default_page_n+1
    text = {}
    page = int(page)
    for docID in canditates[(page-1)*default_page_n : page*default_page_n+1]:
        fin = open("engine/tmp/doc/"+str(docID),"r")
        text[docID] = fin.readlines()
    return render_template("result.html",
        canditates=canditates[(page-1)*default_page_n : page*default_page_n],
        text=text,
        npage=npage,
        page=page)

@app.route('/doc/<docID>', methods=["GET"])
def getDoc(docID):
    fin = open("engine/tmp/doc/"+str(docID),"r")
    text = fin.readlines()
    return render_template("docDisplay.html", text=text)
