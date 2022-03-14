import webbrowser
from flask import *
import hashlib
from pymongo import MongoClient
import requests

#creating DB # database
myclient = MongoClient('localhost',27017)
mydb = myclient["database"]
mycoll=mydb["database"]
app = Flask(__name__, template_folder='./static')
app.secret_key ='f0c0cb26-7024-4331-9de7-c9b7e5fb9e5e'

def GetDataLogin(username, password):
    mycol = mydb["users"]
    password = hashlib.sha512(str(password).encode()).hexdigest()
    data = mycol.find_one({
        "password":password,
        "username":str(username)})
    if not data is None:
        return dict(auth=True,name=data["name"], card=data["card"], date=data["date"], ccv=data["ccv"])
    return dict(auth=False)

def GetDataSumbit(name, card, date,ccv):
    mycol = mydb["users"]
    data = mycol.find_one({
        "name":str(name),
        "card":card,
        "date":str(date),
        "ccv":ccv})
    if not data is None:
        return dict(auth=True,name=data["name"], card=data["card"], date=data["date"], ccv=data["ccv"])
    return dict(auth=False)


@app.route('/')
def index():
        response = render_template('index.html')
       # mongo_relations = mydb.find({}, {'_id': 0, 'service_id': 1, 'beneficiary_id': 1})
        if "username" in session and "password" in session:
            data = GetDataLogin(session["username"], session["password"])
            if data["auth"] == True:
                response = render_template('panel.html',name=data["name"], card=data["card"], date=data["date"], ccv=data["ccv"])
        return response

@app.route('/login', methods=["POST", "GET"])
def LoginRoute():
    data = GetDataLogin(request.form.get("username"), request.form.get("password"))
    if data["auth"] == True:
        session['username'] = request.form.get("username")
        session['password'] = request.form.get("password")
        return redirect("/")
    else:
        return redirect("/#pasword or username is not exist")


@app.route('/logout', methods=["GET"])
def LogoutRoute():
    session['username'] = ''
    session['password'] = ''
    return redirect('/')

@app.route('/sumbitData', methods=["POST", "GET"])
def SumbitRoute():
    name =request.form.get("name")
    card= request.form.get("card")
    date= request.form.get("date")
    ccv =request.form.get("ccv")
    data = GetDataSumbit(name,card ,date,ccv)
    print("createeee")
    if data["auth"] == True:
        session['name'] = name
        session['card'] = card
        session['date'] = date
        session['ccv'] = ccv
        print("succesful!!")

        requests.get("http://localhost:8080/?name={name}")
        return redirect()
    else:
        return redirect("/#one of the details is incorrect, please try again")
app.run(host="127.0.0.1" ,port=3000, debug=True)