import json
from flask import Flask, Response, request, jsonify, render_template, redirect, session
from web3 import Web3
from uuid import uuid1
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

accounts_dict = {"0x4d9D85C55Def094CF730ff5971D0755bE51fC595":"0x05136bf03633f996f58febc2781260033a113395354289710a94e73b37448c7e",
                "0x5C30Af26C549091cB9EcCF92B1C3C8b879bE65B7":"0xbbcc7d17637d33d220277dd326e5f8f0d23a79d8d46b5b34e131606f9037954d",
                "0x1c3943b802E2CE4180508EFefA2D84bFCC0B07c3":"0x64160195ce6084514ddc6813e05f16446ea74d62329bd7db48626a77a443300f",
                "0x8F0b70f2d248043CFCbf21f04c30f6F2c16D4b74":"0x25b089209e0fa872d35d0b2aaab273d89024f956cdb190b2ef82d7aec9a2c98f",
                "0xa17025249189cbB551ca44A45Ac60154ab862E6B":"0xe35ee92a614bbf6f9e8e086a5d3fc01fa83052f7561e29f63d8f0bc0aefac441",
                "0x4f7C9B51883773234928429Ccd10d86Fd6D4de13":"0x341c48905ca1247be3b622e71943b0be90e7a7ea3a873745c01ae9d7a7248a1a",
                "0xE0dA71bB1b1d433a5DDf098F57912b451Af50406":"0x0940d34fe167279069b5867ab08405c6eb51263b9e221486707612ca29be7d96",
                "0x0B358af53CbA8095c3157Ed3429201E56B6f9873":"0x627a3683ba3c25ac69054d6ad4f562fd02a3383d969982d68b6a60255ad5f895",
                "0xd704172D989f724B12a77eE0DD460050d5b53f9a":"0x9e02dbf633397749fe9aad123b3a9749995b71f00b3db31e0989e3078a7b7c2e",
                "0xF35685c43bE5e568C9Cb2BFb894E95f84F0cDB93":"0x02fc65460b42a80d045f9df612cdfe9ed3d86b99d155ec273c272ca85ba8d71c"
                }

accounts_flag = 0
with open("main_transaction_receipt.json", 'r') as f:
    datastore = json.load(f)
    abi = datastore["abi"]
    contract_address = datastore["contract_address"]

app = Flask(__name__)
app.config['SECRET_KEY'] = "15de2e5584da6716f650e3d50fa752cd"
user = w3.eth.contract(address=contract_address, abi=abi)
@app.route("/")
def landing_dashboard():
    property_list = user.functions.getProperty().call()
    data = [len(property_list),property_list]
    return render_template("landing_dashboard.html",data = data)

@app.route("/login")
def login_page():
    return render_template("login_page.html")

@app.route("/proclogin", methods=["POST"])
def login():
    if request.method == "POST":
        user_list = user.functions.getUser().call()
        for i in list(user_list):
            if (str(i[0])==str(request.form["user_id"])):
                session["login_account"] = request.form["user_id"]
                session["login_name"] = i[1]
                print ("login success")
                return redirect("/userdashboard")
        return redirect("/error/user not found")
    return redirect("/error/Bad Request")
@app.route("/error/<error>")
def error_page(error):
    data = error
    return render_template("/error.html",data=data)
    
@app.route("/signup")
def signup_page():
    return render_template("signup_page.html")

@app.route("/procsignup", methods=["POST"])
def signup():
    if request.method == "POST":
        user_name = request.form["name"]
        aadhar = request.form["aadhar"]
        pan = request.form["pan"]
        accounts_flag = len(user.functions.getUser().call())
        user_id = w3.eth.accounts[accounts_flag]
        try:
            user.functions.setUser(user_id,user_name,aadhar,pan).transact({"from":w3.eth.accounts[accounts_flag]})
            data = w3.eth.accounts[accounts_flag]
            accounts_flag+=1
            return render_template("signup_success.html",data = data)
        except Exception as e:
            return redirect(f"/error/{str(e)}")

    return redirect("/error/Bad Request")

@app.route("/userdashboard")
def user_dashboard():
    if ("login_account" in session):
        property_list = user.functions.getProperty().call()
        user_properties = []
        for i in list(property_list):
            if (i[0] == str(session["login_account"])):
                user_properties.append(i)

        data = [session["login_account"],session["login_name"],len(user_properties),user_properties]
        return render_template("user_dashboard.html",data=data)
    
    else:
        return redirect("/login")

@app.route("/addproperty",methods=["POST","GET"])
def add_property():
    if ("login_account" in session):
        if (request.method == "GET"):
            data = [session["login_account"],session["login_name"]]
            return render_template("add_property.html",data=data)
        elif (request.method == "POST"):
            prop_value = str(request.form["prop_value"])
            prop_name = request.form["prop_name"]
            prop_street = request.form["prop_street"]
            prop_district = request.form["prop_district"]
            prop_state = request.form["prop_state"]
            prop_id = str(uuid1())
            prop_owner = session["login_account"]
            try:
                user.functions.addProperty(prop_owner, prop_name, prop_id, prop_street, prop_district, prop_state, prop_value).transact({"from":prop_owner})
                return redirect("/userdashboard")
            except Exception as e:
                return redirect(f"/error/{str(e)}")

    else:
        return redirect("/login")
    
@app.route("/setproperty/<prop_id>")
def set_property(prop_id):
    if ("login_account" in session):
        user.functions.setProperty(prop_id).transact({"from":session["login_account"]})
        return redirect("/userdashboard")
    else:
        return redirect("/login")

@app.route("/viewproperty")
def view_property():
    if ("login_account" in session):
        property_list = user.functions.getProperty().call()
        nonuser_properties = []
        for i in list(property_list):
            if (i[0] != str(session["login_account"])):
                nonuser_properties.append(i)

        data = [session["login_account"],session["login_name"],len(nonuser_properties),nonuser_properties]
        return render_template("view_property.html",data=data)
        # return redirect("/userdashboard")
    else:
        return redirect("/login")

@app.route("/requestproperty/<prop_id>")
def request_property(prop_id):
    if ("login_account" in session):
        user.functions.requestProperty(session["login_account"],prop_id).transact({"from":session["login_account"]})
        return redirect("/viewproperty")
    else:
        return redirect("/login")

@app.route("/sellproperty/<prop_id>")
def sell_property(prop_id):
    if ("login_account" in session):
        user.functions.sellProperty(prop_id).transact({"from":session["login_account"]})
        return redirect("/userdashboard")
    else:
        return redirect("/login")

@app.route("/keepproperty/<prop_id>")
def keep_property(prop_id):
    if ("login_account" in session):
        user.functions.keepProperty(prop_id).transact({"from":session["login_account"]})
        return redirect("/userdashboard")
    else:
        return redirect("/login")

@app.route("/approvedproperty")
def approved_property():
    if ("login_account" in session):
        property_list = user.functions.getProperty().call()
        approved_properties = []
        for i in list(property_list):
            if (i[9] == session["login_account"] and i[10] and i[0] != session["login_account"]):
                approved_properties.append(i)
        data = [session["login_account"],session["login_name"],len(approved_properties),approved_properties]
        return render_template("approved_property.html",data=data)
    else:
        return redirect("/login")

@app.route("/purchaseproperty/<prop_id>")
def purchase_property(prop_id):
    if ("login_account" in session):
        property_list = user.functions.getProperty().call()
        for i in list(property_list):
            if (i[2] == prop_id):
                try:
                    amount_in_wei = w3.toWei(float(i[11])/160000,'ether')
                    nonce = w3.eth.getTransactionCount(session["login_account"])
                    txn_dict = {"to":i[0],"value":amount_in_wei,"gas":2000000,"gasPrice":w3.toWei("20","gwei"),"nonce":nonce}
                    ## signed txn parameters: transaction dictionary, sender accounts private key
                    signed_txn = w3.eth.account.signTransaction(txn_dict, accounts_dict[session["login_account"]])
                    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
                    txn_receipt = w3.eth.getTransactionReceipt(txn_hash)

                    user.functions.updateProperty(prop_id, session["login_account"]).transact({"from":session["login_account"]})

                except Exception as e:
                    return redirect(f"/error/{str(e)}")
                break

        return redirect("/userdashboard")
    else:
        return redirect("/login")

@app.route("/logout")
def logout():
    if ("login_account" in session):
        session.pop("login_account",None)
        session.pop("login_name", None)
        return redirect("/")
    return ("Please login first to logout")

if (__name__ == "__main__"):
    app.run(debug=True)