from flask import Flask, render_template, jsonify, request, session, flash, redirect, url_for
from flask import session
from flask import jsonify
import requests
from DatabaseHelper import dataBase
from DoctorsData import jsonData
from io import BytesIO
import base64
import re
import os
from PIL import Image
import sqlite3
import mysql.connector
from datetime import date
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


appt = []

app = Flask(__name__)
app.secret_key = "Healthify"
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# database configurations
app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'healthify',
                          'password': 'health',
                          'database': 'logindb', }
                          
# PayPal API credentials and endpoints
client_id = os.environ.get('CLIENT_ID')
app_secret = os.environ.get('APP_SECRET')
base_url = {
    'sandbox': 'https://api-m.sandbox.paypal.com',
    'production': 'https://api-m.paypal.com'
}

# allow json body
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_AS_ASCII'] = False



#register user into database
def log_user(req: 'Register') -> None:
    with dataBase(app.config['dbconfig']) as cursor:
        # get the current max userId value from the kart table
        cursor.execute("SELECT MAX(userId) FROM usrinfo")
        result = cursor.fetchone()
        userId = result[0] + 1 if result[0] else 1  # increment by 1 or set to 1 if no previous userId found
        # insert the new user into the usrinfo table
        str = """INSERT INTO usrinfo(userId, name, email, sex, state, city, address, contact, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(str, (userId, req.form['name'], req.form['email'], req.form['sex'], req.form['state'], req.form['city'], req.form['address'], req.form['contact'], req.form['password'], ))
       
#register doctor into database
def log_doctor(req: 'DocRegister') -> None:
    with dataBase(app.config['dbconfig']) as cursor:
        # get the current max docId value from the kart table
        cursor.execute("SELECT MAX(docId) FROM docinfo")
        result = cursor.fetchone()
        docId = result[0] + 1 if result[0] else 1  # increment by 1 or set to 1 if no previous docId found
        docname = str("Dr. "+ req.form['name'])
        print(docname)
        # insert the new user into the docinfo table
        string = """INSERT INTO docinfo(docId, name, email, sex, state, city, address, contact, specialization, description, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(string, (docId, docname, req.form['email'], req.form['sex'], req.form['state'], req.form['city'], req.form['address'], req.form['contact'], req.form['specialization'], req.form['description'], req.form['password'], ))
     
#register pharmacist into database
def log_pharmacist(req: 'PharmaRegister') -> None:
    with dataBase(app.config['dbconfig']) as cursor:
        # get the current max pharmaId value from the kart table
        cursor.execute("SELECT MAX(pharmaId) FROM pharmainfo")
        result = cursor.fetchone()
        pharmaId = result[0] + 1 if result[0] else 1  # increment by 1 or set to 1 if no previous pharmaId found
        # insert the new user into the pharmainfo table
        str = """INSERT INTO pharmainfo(pharmaId, name, email, sex, state, city, address, contact, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(str, (pharmaId, req.form['name'], req.form['email'], req.form['sex'], req.form['state'], req.form['city'], req.form['address'], req.form['contact'], req.form['password'], ))
            
#validate user credentials
def valid_user(req:'login')->int:
    with dataBase(app.config['dbconfig']) as cursor:
       str = """select count(*),name,email,userId from usrinfo where password = %s and email = %s """
       cursor.execute(str,(req.form['password'], req.form['email'], ))
       a = cursor.fetchone()
    return a
    
#validate doctor credentials
def valid_doctor(req:'doctorlogin')->int:
    with dataBase(app.config['dbconfig']) as cursor:
       str = """select count(*),name,email,docId from docinfo where password = %s and email = %s """
       cursor.execute(str,(req.form['password'], req.form['email'], ))
       b = cursor.fetchone()
    return b
    
#validate pharmacist credentials
def valid_pharmacist(req:'pharmalogin')->int:
    with dataBase(app.config['dbconfig']) as cursor:
       str = """select count(*),name,email,pharmaId,city from pharmainfo where password = %s and email = %s """
       cursor.execute(str,(req.form['password'], req.form['email'], ))
       c = cursor.fetchone()
    return c

#booking appointment data
def appoint_data(req: 'Appointment',doc: 'doctor',fee: 'fee') -> None:
    with dataBase(app.config['dbconfig']) as cursor:
        str = """insert into appoint(doc_name,email,patient_name,gender,patient_age,date,time,phn_number,fee) values (%s,%s,%s,%s,%s,%s,%s,%s,%s) """
        cursor.execute(str, (doc,session['email'], req.form['patient_name'], req.form['gender'], req.form['patient_age'], req.form['date'], req.form['time'], req.form['contact'],fee, ))

def getLoginDetails():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        if 'email' not in session:
            loggedIn = False
            firstName = ''
            noOfItems = 0
        else:
            loggedIn = True
            userId = session['userId']
            firstName = session['name']
            cur.execute("SELECT count(productId) FROM kart WHERE userId = ?", (userId, ))
            noOfItems = cur.fetchone()[0]
    conn.close()
    return (loggedIn, firstName, noOfItems)
    
def getDoctorLoginDetails():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        if 'email' not in session:
            loggedIn = False
            firstName = ''
        else:
            loggedIn = True
            docId = session['docId']
            name = session['name']
    conn.close()
    return (loggedIn, name)
    
def getPharmaLoginDetails():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        if 'email' not in session:
            loggedIn = False
            firstName = ''
        else:
            loggedIn = True
            pharmaId = session['pharmaId']
            firstName = session['name']
            city = session['city']
            print(city)
    conn.close()
    return (loggedIn, firstName, city)


@app.route('/')
def home():
   if 'logged_in' not in session:
    return render_template('home.html')
   else:
       return render_template('logout.html')
       
@app.route('/doctorhome')
def doctorhome():
   if 'logged_in' not in session:
    return render_template('home.html')
   else:
       return render_template('doctorlogout.html')
       
@app.route('/pharmahome')
def pharmahome():
   if 'logged_in' not in session:
    return render_template('home.html')
   else:
       email = session['email']
       city = session['city']
       print(email)
       print(city)
       return render_template('pharmalogout.html')

@app.route('/login')
def login(title=""):
    return  render_template('login.html',error = title)
    
@app.route('/doctorlogin')
def doctorlogin(title=""):
    return  render_template('doctorlogin.html',error = title)
    
@app.route('/pharmalogin')
def pharmalogin(title=""):
    return  render_template('pharmalogin.html',error = title)
    
@app.route('/contact',methods=['POST'])
def contact(title=""):
  if session.get('logged_in'):
    log_user(request)
    return  redirect(url_for('contact'))
    
@app.route('/doctorcontact',methods=['POST'])
def doctorcontact(title=""):
  if session.get('logged_in'):
    log_user(request)
    return  redirect(url_for('doctorcontact'))
    
@app.route('/pharmacontact',methods=['POST'])
def pharmacontact(title=""):
  if session.get('logged_in'):
    log_user(request)
    return  redirect(url_for('pharmacontact'))

@app.route('/log',methods=['POST'])
def do_admin_login():
        flag = valid_user(request)
        if flag[0]:
            session['logged_in'] = True
            session['name'] = flag[1]
            session['email'] = flag[2]
            session['userId'] = flag[3]
            return render_template('logout.html')
        else:
            return login(title="wrong username or password!")
            
@app.route('/doctorlog',methods=['POST'])
def do_doctor_login():
        flag = valid_doctor(request)
        if flag[0]:
            session['logged_in'] = True
            session['name'] = flag[1]
            session['email'] = flag[2]
            session['docId'] = flag[3]
            return render_template('doctorlogout.html')
        else:
            return login(title="wrong username or password!")
            
@app.route('/pharmalog',methods=['POST'])
def do_pharma_login():
        flag = valid_pharmacist(request)
        if flag[0]:
            session['logged_in'] = True
            session['name'] = flag[1]
            session['email'] = flag[2]
            session['pharmaId'] = flag[3]
            session['city'] = flag[4]
            return render_template('pharmalogout.html')
        else:
            return login(title="wrong username or password!")
            
@app.route('/signoption',methods=["GET","POST"])
def do_signupoption():
 if not session.get('logged_in'):
    return render_template('SignOption.html')
 else :
     return render_template('home.html')
     
@app.route('/loginoption',methods=["GET","POST"])
def do_loginoption():
 if not session.get('logged_in'):
    return render_template('Loginoption.html')
 else :
     return render_template('home.html')


@app.route('/register',methods=["GET","POST"])
def do_register():
 if not session.get('logged_in'):
    return render_template('register.html')
 else :
     return render_template('home.html')
     
@app.route('/registerdoc',methods=["GET","POST"])
def do_docregister():
 if not session.get('logged_in'):
    return render_template('registerdoc.html')
 else :
     return render_template('home.html')
     
@app.route('/registerpharma',methods=["GET","POST"])
def do_pharmaregister():
 if not session.get('logged_in'):
    return render_template('registerpharma.html')
 else :
     return render_template('home.html')

@app.route('/info',methods=['POST'])
def user_info():
    log_user(request)
    # rqst_name(request)
    return redirect(url_for('home'))
    
@app.route('/docinfo',methods=['POST'])
def doc_info():
    log_doctor(request)
    # rqst_name(request)
    return redirect(url_for('home'))
    
@app.route('/pharmainfo',methods=['POST'])
def pharma_info():
    log_pharmacist(request)
    # rqst_name(request)
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('logged_in')
    return redirect(url_for('home'))

@app.route('/dentist')
def dentist():
    data = jsonData()
    list = data['dentist']
    session['doclist'] = list
    return render_template('card.html',doctors=list)


@app.route('/ENT')
def ENT():
    data = jsonData()
    list = data['ent']
    session['doclist'] = list
    return render_template('card.html', doctors=list)


@app.route('/dermatologist')
def dermatologist():
    data = jsonData()
    list = data['dermo']
    session['doclist'] = list
    return render_template('card.html', doctors=list)


@app.route('/neurologist')
def neurologist():
    data = jsonData()
    list = data['neuro']
    session['doclist'] = list
    return render_template('card.html', doctors=list)


@app.route('/podiatrist')
def podiatrist():
    data = jsonData()
    list = data['pod']
    session['doclist'] = list
    return render_template('card.html', doctors=list)


@app.route('/physicalTherapist')
def physicalTherapist():
    data = jsonData()
    list = data['phy']
    session['doclist'] = list
    return render_template('card.html', doctors=list)


@app.route('/spn',methods=['GET'])
def spn():
    doc = []
    value = request.args["city"]
    list = session['doclist']
    for ls in list:
        if ls['address']['city'] == value:
            doc.append(ls)
    return render_template('card.html',doctors=doc)

@app.route('/book',methods=['GET'])
def book():
    if 'logged_in' not in session:
        return login(title="Please login First")
    else:
        value = request.args['submit']
        data = value.split(',')
        global appt
        appt.append(data[0])
        appt.append(data[2])

        return render_template('booking.html',doctor=data[0],patient=session['email'],time=data[1],fee=data[2])


@app.route('/appointment',methods=['POST'])
def appoint():
    global appt
    appoint_data(request,appt[0],appt[1])
    appt.clear()
    return home()
import mysql.connector

@app.route('/myappointment')
def myappointments():
    loggedIn, firstName, noOfItems = getLoginDetails()
    email = session['email']
    print(email)
    
    cnx = mysql.connector.connect(user='healthify', password='health',
                              host='127.0.0.1',
                              database='logindb')
    cursor = cnx.cursor()
    
    query = "SELECT * FROM appoint JOIN usrinfo ON appoint.email = usrinfo.email WHERE appoint.email = %s"
    cursor.execute(query, (email,))
    rows = cursor.fetchall()
    
    print(rows)

    cursor.close()
    cnx.close()

    return render_template('myappoint.html', rows=rows, loggedIn=loggedIn, firstName=firstName)

  
@app.route('/viewappointments')
def viewappointments():
    loggedIn, firstName = getDoctorLoginDetails()
    name = session.get('name', [])
    print(name)
    #noOfItems = session.get('noOfItems', []
    cnx = mysql.connector.connect(user='healthify', password='health',
                              host='127.0.0.1',
                              database='logindb')
    cursor = cnx.cursor()
    
    query = "SELECT * FROM appoint JOIN docinfo ON appoint.doc_name = docinfo.name WHERE appoint.doc_name = %s"
    cursor.execute(query, (name,))
    rows = cursor.fetchall()
    
    print(rows)

    cursor.close()
    cnx.close()

    return render_template('viewappoint.html', rows=rows, loggedIn=loggedIn, firstName=firstName)
 

@app.route('/ordermedicine')
def order():
    loggedIn, firstName, noOfItems = getLoginDetails()
    #noOfItems = session.get('noOfItems', [])
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT productId, name, price, description, image, stock FROM products')
        itemData = cur.fetchall()
    itemData = parse(itemData)
    return render_template('order.html', itemData=itemData, loggedIn=loggedIn  , noOfItems=noOfItems)
    
@app.route('/myorders')
def myorder():
    loggedIn, firstName, noOfItems = getLoginDetails()
    email = session['email']
    print(email)
    
    cnx = mysql.connector.connect(user='healthify', password='health',
                              host='127.0.0.1',
                              database='logindb')
    cursor = cnx.cursor()
    
    query = ("SELECT deliveryaddress.email, productId, productNames, quantity, noOfItems, price, deliveryaddress.address, deliveryaddress.city, deliveryaddress.state, deliveryaddress.contact_number FROM deliveryaddress JOIN usrinfo ON deliveryaddress.email = usrinfo.email WHERE deliveryaddress.email = %s")

    cursor.execute(query, (email,))
    rows = cursor.fetchall()
    
    print(rows)

    cursor.close()
    cnx.close()

    return render_template('myorders.html', rows=rows, loggedIn=loggedIn, firstName=firstName)

@app.route('/vieworders/')
@app.route('/vieworders')
def vieworder():
    loggedIn, firstName, noOfItems = getPharmaLoginDetails()
    city = session['city']
    print(city)
    
    cnx = mysql.connector.connect(user='healthify', password='health',
                              host='127.0.0.1',
                              database='logindb')
    cursor = cnx.cursor()
    
    query = ("SELECT * FROM deliveryaddress JOIN pharmainfo ON deliveryaddress.city = pharmainfo.city WHERE deliveryaddress.city = %s")

    cursor.execute(query, (city,))
    rows = cursor.fetchall()
    rows1 = [row[1] for row in rows]
    rows2 = [row[2] for row in rows]
    rows3 = [row[3] for row in rows]
    
    #for row in rows:
    # Split items into lists and calculate max length
      #  items1 = row[2].split(',')
      #  items2 = row[3].split(',')
       # max_length = max(len(items1), len(items2))
    
    cursor.close()
    cnx.close()

    return render_template('vieworders.html', rows=rows, loggedIn=loggedIn, firstName=firstName)
  
 
@app.route('/addressdata',methods=['POST']) 
def addressdata() -> None:
    loggedIn, firstName, noOfItems = getLoginDetails()
    with dataBase(app.config['dbconfig']) as cursor:
        name=request.form['name']
        productId = ','.join(map(str, session['productId']))
        productNames = ','.join(map(str, session['productNames']))
        quantity = ','.join(map(str, session['quantity']))
        totalPrice = str(session['totalPrice'])
        totalPrice = totalPrice.split(',')
        totalPrice = ','.join(totalPrice)
        print(productId)
        print(quantity)
        print(totalPrice)
        query = """insert into deliveryaddress(email,productId,productNames,quantity,noOfItems,price,username,address,city,state,contact_number) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
        cursor.execute(query, (session['email'], productId, productNames, quantity, session['noOfItems'], totalPrice, request.form['name'], request.form['address'], request.form['city'], request.form['state'], request.form['contact_number'], ))  
        flash(f'Successfully added the address, {name}!')
    return render_template("deladdress.html", loggedIn=loggedIn, firstName=firstName, patient=session['email'], noOfItems=noOfItems)

@app.route('/deladdress/') 
@app.route('/deladdress',methods=['POST'])
def useraddressdata():
    loggedIn, firstName, noOfItems = getLoginDetails()
    productId = session.get('productId', [])
    productNames = session.get('productNames', [])
    noOfItems = session.get('noOfItems', [])
    quantity = session.get('quantity', [])
    totalPrice = session.get('totalPrice',[])
    totalPrice = round(totalPrice/73.15, 2)
    print(productId)
    print(productNames)
    print(noOfItems)
    print(quantity)
    print(totalPrice)
    return render_template("deladdress.html", loggedIn=loggedIn, firstName=firstName, patient=session['email'], noOfItems=noOfItems, totalPrice=totalPrice)

@app.route('/payment/')
@app.route('/payment',methods=['POST'])
def payment():
    loggedIn, firstName, noOfItems = getLoginDetails()
    # Call the capture_paypal_order() method to store the capture_data in the session object
    #capture_paypal_order()

# Retrieve the capture_data from the session object and convert it to JSON format
    #json_data = jsonify(session['capture_data'])

    #payment_details = request.get_json(),
    response = session.get('capture_data',{})
    response = jsonify(response)
    transaction_id = session.get('transaction_id')
    transaction_id = jsonify(transaction_id)
    #print(payment_details)
    totalPrice = session.get('totalPrice',[])
    print(totalPrice)
    print(response)
    print(transaction_id)
    return render_template("payment.html", loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems, totalPrice=totalPrice, response=response, transaction_id=transaction_id)
  
@app.route("/productDescription")
def productDescription():
    loggedIn, firstName, noOfItems = getLoginDetails()
    productId = request.args.get('productId')
    print(productId)
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT productId, name, price, description, image, stock FROM products WHERE productId = ?', (productId, ))
        productData = cur.fetchone()
        stock = productData[5]
        print(stock)
    conn.close()
    data=productData
    return render_template("productDescription.html", data=productData, loggedIn=loggedIn, noOfItems=noOfItems)

@app.route('/addtocart', methods=['POST'])
def ADDTOCART():
    # Check if the user is logged in
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    # Get the product ID and quantity from the request
    productId = request.form.get('productId')
    session['productIdnew'] = productId
    print(productId)
    quantity = request.form.get('quantity')
    quantity = int(quantity)
    # Connect to the database and retrieve the user's cart item for the specified product
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        userId = session['userId']
        if productId == productId:
            cur.execute('SELECT * FROM kart WHERE userId = ? AND productId = ?', (userId, productId))
            cart_item = cur.fetchone()
            if cart_item:
                quantity = cart_item[2] + quantity
                cur.execute('UPDATE kart SET quantity = ? WHERE userId = ? AND productId = ?', (quantity, userId, productId))
                conn.commit()
                cur.execute('SELECT * FROM kart WHERE userId = ? AND productId = ?', (userId, productId))
                cart_item = cur.fetchone()
                session['cart_itemnew'] = cart_item
                #quantity = cart_item[2] + quantity
                print(cart_item)
            else:
                cur.execute('INSERT INTO kart (userId, productId, quantity) VALUES (?, ?, ?)', (userId, productId, quantity))
                cur.execute('SELECT * FROM kart WHERE userId = ? AND productId = ?', (userId, productId))
                cart_item = cur.fetchone()
                session['cart_item'] = cart_item
                conn.commit() 
                print(cart_item) 
                  
    # Print a message to verify that the function completed successfully
    print('Product added to cart successfully') 
    # Return a response to render the order.html template with the cart item data
    return render_template("order.html",data=cart_item)

@app.route('/ordercart/')
@app.route('/ordercart', methods=['POST'])
def cart():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    productId = request.form.get('productId')
    session['productIdnew'] = productId
    print(productId)
    quantity = request.form.get('quantity')
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        userId = session['userId']
        item = session.get('cart_item', [])
        itemnew = session.get('cart_itemnew', [])
        newproductid = session.get('productIdnew', [])
        print(item)
        print(itemnew)
        print(newproductid)
        cur.execute("SELECT products.productId, products.name, products.price, products.image, kart.quantity FROM products, kart WHERE products.productId = kart.productId AND kart.userId = ?", (userId, ))
        products = cur.fetchall()
        cur.execute('UPDATE kart SET quantity = ? WHERE userId = ? AND productId = ?', (quantity, userId, productId))
        #cur.execute('SELECT * FROM kart WHERE userId = ? AND productId = ?', (userId, productId))
        #cart_item=cur.fetchone()
        #print(cart_item)
        session['productId'] = [row[0] for row in products]
        session['productNames'] = [row[1] for row in products]
        itemnames = session['productNames']
        product_ids = session['productId']
        session['noOfItems'] = len(product_ids)
        session['quantity'] = [row[4] for row in products]
        #quantity = session['quantity']
        print(session['productId'])
        print(session['productNames'])
        print(session['noOfItems'])
        print(session['quantity'])
    totalPrice = 0
    for row in products:
        totalPrice += row[2]*row[4]
        totalPrice = round(totalPrice, 2)
        session['price'] = [row[2] for row in products]
        session['totalPrice'] = totalPrice
    return render_template("cart.html", products=products, item=item, itemnew=itemnew, newproductid=newproductid, itemnames=itemnames, totalPrice=totalPrice, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)

@app.route("/removeFromCart",methods=['GET'])
def removeFromCart():
    if 'email' not in session:
        return redirect(url_for('login'))
    email = session['email']
    productId = int(request.args.get('remove'))
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        userId = session['userId']
        try:
            cur.execute("DELETE FROM kart WHERE userId = ? AND productId = ?", (userId, productId))
            conn.commit()
            msg = "removed successfully"
        except:
            conn.rollback()
            msg = "error occured"
    conn.close()
    return redirect(url_for('order'))
    
# create a new order
@app.route('/create-paypal-order', methods=['POST'])
def create_paypal_order():
    order = create_order()
    return jsonify(order)

# capture payment & store order information or fullfill order
@app.route('/capture-paypal-order', methods=['POST'])
def capture_paypal_order():
    order_id = request.json['orderID']
    capture_data = capture_payment(order_id)
    transaction_id = capture_data['purchase_units'][0]['payments']['captures'][0]['id']
    session['capture_data'] = jsonify(capture_data)
    session['transaction_id'] = transaction_id
    # TODO: store payment information such as the transaction ID
    return jsonify(capture_data)

# use the orders api to create an order
def create_order():
    access_token = generate_access_token()
    url = base_url['sandbox'] + '/v2/checkout/orders'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    data = {
        'intent': 'CAPTURE',
        'purchase_units': [
            {
                'amount': {
                    'currency_code': 'USD',
                    'value': '100.00'
                }
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

# use the orders api to capture payment for an order
def capture_payment(order_id):
    access_token = generate_access_token()
    url = base_url['sandbox'] + f'/v2/checkout/orders/{order_id}/capture'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.post(url, headers=headers)
    session['response']=response.json()
    response.raise_for_status()
    print(response.json())
    return response.json()

# generate an access token using client id and app secret
def generate_access_token():
    auth = f'{AfWaprPaO57fffnTzz14gIky7qEmrU46HZVfo6-L1zQnNEnWKZ1qhaMok8aptXU8Dds82ZZ93KuGd_o6}:{EIB9FfsNFgKqsv4gn08qItnRx3hElkXenJo49gX7c2oZ3N_y4HQRwI3FNRV2ZHhuU6pkZ1WeOEUKShF9}'.encode('utf-8')
    headers = {
        'Authorization': 'Basic ' + auth.hex()
    }
    data = {
        'grant_type': 'client_credentials'
    }
    response = requests.post(base_url['sandbox'] + '/v1/oauth2/token', headers=headers, data=data)
    response.raise_for_status()
    return response.json()['access_token']
    
@app.route("/orderPlaced")
def opl():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('Delete from kart where 1=1')
    conn.close()
    return redirect(url_for('order'))

@app.route('/<string:page_name>/')
def rend(page_name):
  return render_template('%s.html' % page_name)

def parse(data):
    ans = []
    i = 0
    while i < len(data):
        curr = []
        for j in range(5):
            if i >= len(data):
                break
            curr.append(data[i])
            i += 1
        ans.append(curr)
    return ans

if __name__ == '__main__':
    app.run(debug=True)