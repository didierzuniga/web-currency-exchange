# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, flash, redirect
import urllib2
import ast

app = Flask(__name__)
app.secret_key = 'some_secret'
app.debug = True

@app.route(r"/", methods=["GET"])
def home():
	return render_template("index.html")

@app.route(r"/convert",methods=["GET"])
def convert():
	return render_template("convert.html")

@app.route(r'/forecast', methods=['GET'])
def forecast():
    return render_template('forecast.html')

def initial():
	print("::::::::::::::::::::::::::::::::::::::")
	print(":: C U R R E N C Y  E X C H A N G E ::")
	print("::::::::::::::::::::::::::::::::::::::\n")
	print("""¿Que deseas cambiar?
	1) MXN a USD
	2) USD a MXN
	3) MXN a JPY
	4) JPY a MXN""")
	valor = input("->")
	if valor != "1" and valor != "2" and valor != "3" and valor != "4":
		print("¡Caracter no permitido!")
	else:
		ammount = int(input("Cantidad a cambiar-> "))
		exchange(valor, ammount)

def exchange(valor, ammount):
	if int(valor) == 1:
		b = "MXN"
		f = "USD"
	elif int(valor) == 2:
		b = "USD"
		f = "MXN"
	elif int(valor) == 3:
		b = "MXN"
		f = "JPY"
	elif int(valor) == 4:
		b = "JPY"
		f = "MXN"

	path = "https://api.fixer.io/latest?base=%s" %(b)
	response = urllib2.urlopen(path)
	data = response.read()
	drt = ast.literal_eval(data)
	print("_____________________________________\n")
	print(" Tarifa al día: {}".format(drt["date"]))
	result = ammount * drt["rates"][f]
	print(" Su cambio es ${} {}".format(result, f))
	print("_____________________________________\n")

if __name__ == '__main__':
	app.run()