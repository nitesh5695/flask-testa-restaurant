from flask import Flask,render_template,request,session,redirect,url_for
import pyrebase
app=Flask(__name__)
app.secret_key="Nitesh@1234"
config={    "apiKey": "AIzaSyC-x73AHgduv4CTXeYJu4rTjnrwDfj1yls",
    "authDomain": "enterschool-a70f5.firebaseapp.com",
    "databaseURL": "https://enterschool-a70f5.firebaseio.com",
    "projectId": "enterschool-a70f5",
    "storageBucket": "enterschool-a70f5.appspot.com",
    "messagingSenderId": "408802600224",
    "appId": "1:408802600224:web:3fe1983eb48f8cc0c4a345",
    "measurementId": "G-PVJMPYECRW"
    }
firebase=pyrebase.initialize_app(config)
auth=firebase.auth()
db=firebase.database()
@app.route('/')
def login_page():
    return render_template('index.html')
@app.route('/home')
def home():
    try:
        user=session['username']
        return render_template('home.html')
    except:
        return render_template("index.html",message="please login first")
@app.route('/login_validate',methods=['POST']) 
def login_validate():
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')
        session['username']=email
        session['pass']=password
        if session['username']and session['pass']:
            try:
                
                user=auth.sign_in_with_email_and_password(email,password)
                return redirect(url_for('home'))
            except:
                return render_template('index.html',error="invalid username or password")
        else:
                return render_template('index.html')
    else:
        return render_template('index.html',error="something wrong with form posting")
@app.route("/logout")
def logout():
    session.pop('username',None)
    session.pop('pass',None)
    return render_template('index.html',error="Logout successful")
@app.route('/create_customer')
def create_customer():
    try:
        user=session['username']
        return render_template('create_customer.html')
    except:
        return render_template('index.html')
    return render_template('create_customer.html')
@app.route('/upload_customer_data', methods=['POST'])
def upload_customer_data():
    if request.method=='POST':
        name=request.form.get('name')
        gender=request.form.get('gender')
        mobile=request.form.get('mobile')
        items=request.form.get('items')
        price=request.form.get('price')
        tip=request.form.get('tip')
        pay_mode=request.form.get('pay_mode')
        address=request.form.get('address')
        data={"name":name,
        "mobile":mobile,
        "gender":gender,
        "items":items,
        "price":price,
        "tip":tip,
        "pay_mode":pay_mode,
        "address":address
            }
        customer=db.child('customer').child(mobile).get()
        if customer.val()==None:
            db.child('customer').child(mobile).set(data)
            return render_template('create_customer.html',message='successfully customer created')
            
        else:    
            return render_template('create_customer.html',message='customer already exist')
@app.route('/edit_customer')
def edit_customer():
    try:
        user=session['username']
        return render_template('edit_customer.html')
    except:
        return render_template('index.html')
@app.route('/edit_customer_data',methods=['POST'])
def edit_customer_data():
    if request.method=='POST':
        name=request.form.get('name')
        mobile=request.form.get('mobile')
        update_name=request.form.get('update_name')
        value=request.form.get('value')
        data={update_name:value
            }
        customer=db.child('customer').child(mobile).get()
        if customer.val()==None:
            return render_template('edit_customer.html',message='customer does not exist')
        else:    
            db.child('customer').child(mobile).update(data)
            return render_template('edit_customer.html',message='successfully updated')
     
@app.route('/delete_customer')
def delete_customer():
    try:
        user=session['username']
        return render_template('delete_customer.html')
    except:
        return render_template('index.html')
@app.route('/delete_customer_data',methods=['POST'])
def delete_customer_data():
    if request.method=='POST':
        name=request.form.get('name')
        mobile=request.form.get('mobile')
        try:
            customer=db.child('customer').child(mobile).get()
            if customer.val()==None:
               return render_template('delete_customer.html',message='customer does not exist')
            else:
               db.child('customer').child(mobile).remove()
               return render_template('delete_customer.html',message="successfully deleted")
        except:
          return render_template('delete_customer.html',message="not deleted something wrong with database")
@app.route('/view_customer')
def view_customer():
    try:
        user=session['username']
        customer=db.child('customer').get()
        data=customer.val()
        
        return render_template('view_customer.html',customers=data.values())
    except:    
        return render_template('index.html')
@app.route('/search_customer',methods=['POST'])
def search_customer():
    if request.method=="POST":
        customer_name=request.form.get('search')
        customer=db.child("customer").order_by_child("name").equal_to(customer_name).get()
        print("data get")
        try:
            data=customer.val()
            return render_template('view_customer.html',customers=data.values())
        except:    
            
            #print(data.values())
            return render_template('view_customer.html',message="no data matched")    
if __name__=='__main__':
    app.run(debug=True)
