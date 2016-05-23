# -*- coding: utf-8 -*-
import os

def Extractor(dir):
    files = os.listdir(dir)
    if not (os.path.exists("tmp")):
        os.mkdir("tmp")
    if not (os.path.exists("tmp/doc")):
        os.mkdir("tmp/doc")
    titleFile = open("tmp/title","w")
    for name in files:
        doc = open(dir+"/"+name)
        content = doc.readlines()
        output = open("tmp/doc/"+name.replace(".html",""),"w")
        titleFile.write(name+" : "+content[0].replace("&lt;","<"))
        output.write("Title: "+content[0].replace("&lt;","<"))
        output.write("ID: "+name.replace(".html","")+"\n")
        for i in range(len(content)):
            content[i] = " "+content[i].strip()
        output.write("passage: "+"".join(content[1:]))



if __name__=="__main__":
    Extractor("../Reuters")