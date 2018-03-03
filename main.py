# -*- coding: utf-8 -*-

import urllib2
import ast
from flask import Flask, render_template, request, flash, redirect
from contact_model import Contact

app = Flask(__name__)
app.secret_key = 'some_secret'
app.debug = True

@app.route(r"/", methods=["GET"])
def contact_book():
	contacts = Contact.query().fetch()
	return render_template("contact_book.html", contacts=contacts)

@app.route(r"/add", methods=["GET", "POST"])
def add_contact():
	if request.form:
		contact = Contact(name=request.form.get("name"),
						  phone=request.form.get("phone"),
						  email=request.form.get("email"))
		contact.put()
		flash("¡Se añadió el contacto!")
	return render_template("add_contact.html")

@app.route(r'/contacts/<uid>', methods=['GET'])
def contact_details(uid):
    contact = Contact.get_by_id(int(uid))
    if not contact:
        return redirect('/', code=301)

    return render_template('contact.html', contact=contact)

@app.route(r'/delete', methods=['POST'])
def delete_contact():
    contact = Contact.get_by_id(int(request.form.get('uid')))
    contact.key.delete()
    return redirect('/contacts/{}'.format(contact.key.id()))

def initial():
	print("::::::::::::::::::::::::::::::::::::::")
	print(":: C U R R E N C Y  E X C H A N G E ::")
	print("::::::::::::::::::::::::::::::::::::::\n")
	print("""¿Que deseas cambiar?
	1) MXN a USD
	2) USD a MXN
	3) MXN a JPY
	4) JPY a MXN""")
	valor = raw_input("->")
	if valor != "1" and valor != "2" and valor != "3" and valor != "4":
		print("¡Caracter no permitido!")
	else:
		ammount = int(raw_input("Cantidad a cambiar-> "))
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