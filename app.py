#Main Application

'''
index.html - login page
upload.html - choose and upload file
preview.html - view uploaded files/ delete or run tesseract
display.html - view the result after ocr , edit fields / confirm entry
'''

import os
#from tess import run
from flask import Flask,request,render_template,send_from_directory,redirect,url_for,redirect
import pymysql
import queries
import tesseract

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

qr = queries.sql_queries()
a= tesseract.tess_ocr()
class Database:
    def __init__(self):
        host = "127.0.0.1"
        user = "Sujay"
        password = "laferrar1"
        db = "mydatabase"
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()
    def list(self):
        self.cur.execute("SELECT * FROM PREVIEW")
        result = self.cur.fetchall()
        return result
    def listbb(self):
        self.cur.execute("SELECT * FROM listb")
        result = self.cur.fetchall()
        return result
        
#Login page
@app.route('/',methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['user'] != 'admin' or request.form['pass'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return render_template("upload.html")
    return render_template('index.html', error=error)
    
@app.route('/upload')
def upload_func1():
    return render_template('upload.html')

#Upload page
@app.route('/upload',methods=["POST", "GET"])
def upload_func():
    target = os.path.join(APP_ROOT,'images/')
    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist('file'):
        print(file)
        filename = file.filename
        destination = "/".join([target,filename])
        file.save(destination)
    qr.insert_preview(filename)
    return redirect(url_for('preview_func'))


#Send image file from directory
@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images",filename)

#preview page
@app.route('/preview',methods=['GET','POST'])
def preview_func():
    if request.method == 'GET':
        def preview_list():
            db = Database()
            lst=db.list()
            return lst
    
    elif request.method=='POST':
        if request.form['delete'] == 'Delete':
            id = request.args.get('id')
            qr.delete_preview(id)
            return redirect(url_for('preview_func'))

    res = preview_list()
    return render_template('preview.html', result = res, content_type = "application/json")


#OCR page
@app.route('/display', methods = ['GET','POST'])
def display_func():
    id = request.args.get('id')
    filename = qr.get_filename(id)
    send_image(filename)
    val = a.run_tesseract(filename)
    return render_template('display.html', image_name = filename, retailer_name=val['retailer_name'], 
customer_name=val['customer_name'], order_date = val['order_date'], order_number = val['order_number'],
billing_address = val['billing_address'])

@app.route('/listb')
def list_func():
    return render_template('list.html')

@app.route('/list', methods = ['POST', 'GET'])
def listb_func():    
    def b_list():
        db = Database()
        lst=db.listbb()
        return lst
    if request.method == 'POST':
        if request.form['save_ocr'] == 'SAVE':
            order_number_m = request.form['order_number_mod']
            customer_name_m = request.form['customer_name_mod']
            retailer_name_m = request.form['retailer_name_mod']
            order_date_m = request.form['order_date_mod']
            billing_address_m = request.form['billing_address_mod']

            order_number=request.args['order_number']
            customer_name=request.args['customer_name']
            retailer_name=request.args['retailer_name']
            order_date=request.args['order_date']
            billing_address=request.args['billing_address']
            if not order_number_m:
                ord_num = order_number
            else:
                ord_num = order_number_m
                
            if not customer_name_m:
                cust_name = customer_name
            else:
                cust_name = customer_name_m
            
            if not retailer_name_m:
                ret_name = retailer_name
            else:
                ret_name = retailer_name_m
                
            if not order_date_m:
                ord_date = order_date
            else:
                ord_date = order_date_m
            
            if not billing_address_m:
                bill_add = billing_address
            else:
                bill_add = billing_address_m              
            qr.insert_listb(ord_num, cust_name, ret_name, ord_date, bill_add) 
            return redirect(url_for('listb_func'))    
    res = b_list()     
    return render_template('b.html', result= res, content_type = "application/json")

if __name__ == "__main__":
    app.run(debug=True)
