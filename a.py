from flask import Flask, render_template,json,request,redirect,url_for,flash
from flask_restful import Resource,Api
import webbrowser
import flask
import os

from PIL import Image
import sys
import random
import math
import numpy as np
import skimage.io



import subprocess

d=open("mask.txt","r")


app=Flask(__name__)
api=Api(app)
app.secret_key = 'the random string'

@app.route('/',methods = ['GET', 'POST'])
def index():
    return render_template("base.html")


@app.route('/ver',methods = ['GET', 'POST'])
def ver():
    return render_template("ver.html")


@app.route('/hor',methods = ['GET', 'POST'])
def hor():
    return render_template("hor.html")

@app.route('/mask',methods = ['GET', 'POST'])
def mask():
    return render_template("mask.html")
@app.route('/analyse/add',methods = ['GET', 'POST'])
def analyse():
    return render_template("analyse.html")

@app.route("/add", methods=["POST"])
def add():
    Path = request.form.get("Path")
    Original_Image = Image.open(Path)

    rotated_image1 = Original_Image.rotate(180)
    file_name = os.path.basename(Path)

    a=file_name.split('.')
    print(a[0])
    


    rotated_image1.save('dataset/Image/vertical/'+a[0]+'.png') 

    return flask.send_file('dataset/Image/vertical/'+a[0]+'.png', mimetype='image/png')



    return redirect(url_for("/hor"))


@app.route("/add1", methods=["POST"])
def add1():
    Path = request.form.get("Path")
    Original_Image = Image.open(Path)

    img = Image.open(Path)

# get width and height
    width = img.width
    height = img.height

# display width and height
    print("The height of the image is: ", height)
    print("The width of the image is: ", width)
    
   

    rotated_image1 = Original_Image.rotate(180)
    file_name = os.path.basename(Path)

    a=file_name.split('.')
    print(a[0])

    if width>height:
        flash("It is already on horizontal Image")
        return redirect(url_for("hor"))

    else:
    


        rotated_image1.save('dataset/Image/horizontal/'+a[0]+'.png') 

        return flask.send_file('dataset/Image/horizontal/'+a[0]+'.png', mimetype='image/png')



    return redirect(url_for("index"))

@app.route("/add2", methods=["POST"])
def add2():
    Path = request.form.get("Path")
    Original_Image = Image.open(Path)

    file_name = os.path.basename(Path)
    import shutil
    shutil.copy(Path,'.')

    

    subprocess.call("PixelIterator.py", shell=True)
    return "jgfk"




        








if __name__ == '__main__':
    app.debug = True
    url="http://127.0.0.1:"+str(8089)+"/"
    webbrowser.open_new(url)
    app.run(host="0.0.0.0",port=8089) #host="0.0.0.0" will make the page accessable
                            #by going to http://[ip]:5000/ on any computer in 
                            #the network.

 # importing cv



 