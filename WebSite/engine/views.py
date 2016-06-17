import cPickle as pickle
import os
from flask import render_template, request, redirect, url_for

from config.config import config
from engine import app
from engine.query import load_and_calc
from engine.dic import parse, Info

default_page_n = 10

if not os.path.exists(config.TIERED_INDEX_FILE) or not os.path.exists(config.ID_HTML_FILE):
    info, id_html = parse()
    tiered_index_file = open(config.TIERED_INDEX_FILE, 'w')
    pickle.dump(info, tiered_index_file, config.PICKLE_PROTOCOL)
    id_html_file = open(config.ID_HTML_FILE, 'w')
    pickle.dump(id_html, id_html_file, config.PICKLE_PROTOCOL)

pkl_file = open(config.TIERED_INDEX_FILE, 'r')
info = pickle.load(pkl_file)
index, voc, entries = load_and_calc(info)

pkl_file = open(config.ID_HTML_FILE, 'r')
id_html = pickle.load(pkl_file)


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
