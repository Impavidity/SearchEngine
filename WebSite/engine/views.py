from engine import app
from flask import render_template, request, redirect, url_for

@app.route('/',methods=["POST","GET"])
def index():
    if request.method == "GET":
        return render_template("home.html")
    if request.method == "POST":
        queryWords = request.form["iQuery"]
        
        return redirect(url_for("result"))

@app.route('/result', methods=["GET","POST"])
def result():
    return render_template("result.html")
