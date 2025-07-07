"""
DEPRECATED: This file has been replaced by app.py
The new version includes:
- Better security (CSRF protection, input validation)
- Modular architecture (separated models, forms, services)
- Improved error handling and logging
- Caching for better performance
- Type hints and documentation
- Configuration management

Please use: python app.py instead of python main.py
"""

from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators,SelectField,IntegerField
from passlib.hash import sha256_crypt
from flask_wtf import FlaskForm
from functools import wraps
from wtforms.validators import DataRequired


class RegisterForm(Form):
    name = StringField("Name Surname:",validators=[validators.Length(min=5,max=30)])
    uname = StringField("Username:",validators=[validators.Length(min=5,max=20)])
    email = StringField("Email:",validators=[validators.Length(min=5,max=20)])
    pwd = PasswordField("Password:",validators=[
    validators.DataRequired(message="Please check your password!"),
    validators.EqualTo(fieldname="confirm",message="Check your password!")
    ])
    confirm = PasswordField("Password Correct:")


app = Flask(__name__)
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]=""
app.config["MYSQL_DB"]="coronablog"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
app.secret_key="corona"

mysql = MySQL(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            if session["status"] == 1:
                return f(*args, **kwargs)
            return redirect(url_for("blog"))

        else:
            flash("You are not allowed to view this page","danger")
            return redirect(url_for("blog"))
    return decorated_function

@app.route("/")
def index():
    return render_template("index.html",form=PolynomialRegression(),date=dates())

def dates():
    from datetime import datetime,date 
    from datetime import timedelta  

    today = date.today()
    todaylisted = list()
    for i in range(0,7):
        todaylisted.append(today + timedelta(days=i+1))
    return todaylisted


@app.route("/information",methods=["GET","POST"])
def information():
    if request.method =="POST":
        pass
    else:
        return render_template("information.html",data=coronaTotalData(),countrydata=coronaCountryData())
    

@app.route("/dashboard")
@login_required
def dashboard():
    cursor = mysql.connection.cursor()
    query = "Select * from articles"
    result = cursor.execute(query,)
    if result >0:
        articles = cursor.fetchall()
        return render_template("dashboard.html",articles=articles)
    else:

        return render_template("dashboard.html")

@app.route("/contactmessage")
@login_required
def contactmessages():
    cursor = mysql.connection.cursor()
    query = "Select * from contact"
    result = cursor.execute(query,)
    if result >0:
        messages = cursor.fetchall()
        return render_template("contactmessage.html",messages=messages)
    else:

        return render_template("contactmessage.html")

@app.route("/blog",methods=["GET","POST"])
def blog():
    if request.method=="POST":
        try:
            cur = mysql.connection.cursor()
        except:
            flash("Server connection failed","danger")
            return redirect(url_for("blog"))
        uname = request.form['username']
        pwd = request.form['password']
        query = "Select * from user where uname =%s"
        result = cur.execute(query,(uname,))
        if result>0:
            data = cur.fetchone()
            password = data['pwd']
            status = data['status']
            if sha256_crypt.verify(pwd,password):
                
                session["logged_in"] = True
                session["uname"] = uname
                session['status'] = status
                return redirect(url_for("blog"))
            else:
                flash("Your password is wrong","danger")
                return redirect(url_for("blog"))
        else:
            flash("No such user","danger")
            return redirect(url_for("blog"))
    else:
        try:
            cursor = mysql.connection.cursor()
        except:
            flash("Server connection failed","danger")
            return render_template("blog.html")
        query = "select * from articles"
        result = cursor.execute(query)
        if result>0:
            articles = cursor.fetchall()
            return render_template("blog.html",articles =articles)
        else:
            return render_template("blog.html")
    


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You successfully logged out","success")
    return redirect(url_for("blog"))


@app.route("/register",methods=["GET","POST"])
def register():
    form = RegisterForm(request.form)
    if request.method=="POST" and form.validate():
        uname = form.uname.data
        name = form.name.data
        email = form.email.data
        pwd = sha256_crypt.encrypt(form.pwd.data)
        cursor = mysql.connection.cursor()
        query = "Select * from user where uname =%s"
        cursor.execute(query,(uname,))
        data = cursor.fetchone()
        try:
            if data['uname'] in uname:
                flash("Böyle bir kullanıcı var","danger")
                return redirect(url_for("blog"))
        except:
            query = "Insert into user (name,email,uname,pwd) values (%s,%s,%s,%s)"
            cursor.execute(query,(name,email,uname,pwd))
            mysql.connection.commit()
            cursor.close()       
            flash("You have successfully registered","success")
            return redirect(url_for("blog"))
    else:
        return render_template("register.html",form=form)


@app.route("/addarticle",methods=["GET","POST"])
@login_required
def addarticle():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["article"]
        keywords = request.form["keywords"]
        cursor = mysql.connection.cursor()
        query = "Insert into articles (title,author,content,keywords) VALUES (%s,%s,%s,%s)"
        cursor.execute(query,(title,session["uname"],content,keywords))
        mysql.connection.commit()
        cursor.close()
        flash("Article Successfully Added","success")
        return redirect(url_for("dashboard"))
    return render_template("addarticle.html")


@app.route("/contact",methods=["GET","POST"])
def contact():
    if request.method=="POST":
        email = request.form["email"]
        name = request.form["name"]
        surname = request.form["surname"]
        message = request.form["message"]
        cursor =mysql.connection.cursor()
        query = "Insert into contact (email,name,surname,message) VALUES (%s,%s,%s,%s)"
        cursor.execute(query,(email,name,surname,message))
        mysql.connection.commit()
        cursor.close()
        flash("Message Sent Successfully","success")
        return redirect(url_for("contact"))
    else:
        return render_template("contact.html")

@app.route("/blog/<string:id>")
def detail(id):
    cursor = mysql.connection.cursor()
    query = "select * from articles where id = %s"
    result = cursor.execute(query,(id,))
    if result>0:
        article = cursor.fetchone()
        return render_template("detail.html",article=article)
    else:
        return render_template("detail.html")

def coronaCountryData():
    import http.client
    import json
    conn = http.client.HTTPSConnection("api.collectapi.com")
    headers = {
    'content-type': "application/json",
    'authorization': "apikey ENTER YOUR API KEY HERE"
    }
    conn.request("GET", "/corona/countriesData", headers=headers)
    res = conn.getresponse()
    res = res.read()
    res = json.loads(res)
    res = res['result']
    return res

@app.route("/ban/<string:id>")
@login_required
def userban(id):
    cursor = mysql.connection.cursor()
    query = "select * from user where id =%s"
    result = cursor.execute(query,(id,))
    if result>0:
        query2 ="update user Set status = %s where id =%s "
        cursor = mysql.connection.cursor()
        cursor.execute(query2,(2,id))
        mysql.connection.commit()
        flash("User Blocked!","success")
        return redirect(url_for("usersettingsdash"))

@app.route("/removeban/<string:id>")
@login_required
def userremoveban(id):
    cursor = mysql.connection.cursor()
    query = "select * from user where id =%s"
    result = cursor.execute(query,(id,))
    if result>0:
        query2 ="update user Set status = %s where id =%s "
        cursor = mysql.connection.cursor()
        cursor.execute(query2,(0,id))
        mysql.connection.commit()
        flash("User Unblocked!","success")
        return redirect(url_for("usersettingsdash"))

@app.route("/makeadmin/<string:id>")
@login_required
def makeadmin(id):
    cursor = mysql.connection.cursor()
    query = "select * from user where id =%s"
    result = cursor.execute(query,(id,))
    if result>0:
        query2 ="update user Set status = %s where id =%s "
        cursor = mysql.connection.cursor()
        cursor.execute(query2,(1,id))
        mysql.connection.commit()
        flash("User is in admin status","success")
        return redirect(url_for("usersettingsdash"))


@app.route("/delete/<string:id>")
@login_required
def delete(id):
    cursor = mysql.connection.cursor()
    query = "select * from articles where id = %s"
    result = cursor.execute(query,(id,))
    if result >0:
        query2= "delete from articles where id =%s"
        cursor.execute(query2,(id,))
        mysql.connection.commit()
        return redirect(url_for("dashboard"))
    else:
        flash("No article","danger")
        return redirect(url_for("index"))

@app.route("/edit/<string:id>",methods=["GET","POST"])
@login_required
def update(id):
    if request.method =="GET":
        cursor = mysql.connection.cursor()
        query = "select * from articles where id =%s"
        result = cursor.execute(query,(id,))
        if result ==0:
            flash("No article","danger")
            return redirect(url_for("dashboard"))
        else:
            article = cursor.fetchone()
            return render_template("update.html",request=article)
    else:
        newtitle = request.form["title"]
        newcontent = request.form["article"]
        newkeywords = request.form["keywords"]
        query2 = "update articles Set content = %s , title =%s , keywords=%s  where id = %s"
        cursor = mysql.connection.cursor()
        cursor.execute(query2,(newcontent,newtitle,newkeywords,id))
        mysql.connection.commit()
        flash("article successfully updated","success")
        return redirect(url_for("dashboard"))

@app.route("/usersettings")
@login_required
def usersettingsdash():
    cursor = mysql.connection.cursor()
    query = "Select * from user"
    result = cursor.execute(query,)
    if result >0:
        articles = cursor.fetchall()
        return render_template("usersettings.html",articles=articles)
    else:
        return render_template("usersettings.html")

def coronaTotalData():
    import http.client
    import json
    conn = http.client.HTTPSConnection("api.collectapi.com")
    headers = {
    'content-type': "application/json",
    'authorization': "apikey ENTER YOUR API KEY HERE"
        }
    conn.request("GET", "/corona/totalData", headers=headers)
    res = conn.getresponse()
    data = res.read()
    data = json.loads(data)
    return data

_date=190
 
def PolynomialRegression():
    import pandas as pd
    import numpy as np
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import PolynomialFeatures
    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()

    df = pd.read_excel('static/dataset/turkey.xlsx')
    cases = df.Cases.values.reshape(-1,1)
    death = df.Deaths.values.reshape(-1,1)
    date = df.iloc[:,3:4].values
    date[:,0] = le.fit_transform(date[:,0])

    poly_reg = PolynomialFeatures(degree=5)
    X_poly = poly_reg.fit_transform(date)
    pol_reg = LinearRegression()
    pol_reg.fit(X_poly, cases)


    polys_reg = PolynomialFeatures(degree=5)
    Y_poly = polys_reg.fit_transform(date)
    polz_reg = LinearRegression()
    polz_reg.fit(Y_poly, death)      
    coronapredictlist = list()
    deathpredictlist = list()
    for i in range(_date,_date+7):
        coronapredictlist.append(int(pol_reg.predict(poly_reg.fit_transform([[i]]))))
        deathpredictlist.append(int(polz_reg.predict(polys_reg.fit_transform([[i]]))))
    
    return coronapredictlist,deathpredictlist


@app.route("/news")
def news():
    return render_template("news.html",coronanews=coronaNews(),coronacount=len(coronaNews()))



def coronaNews():
    import http.client
    import json
    conn = http.client.HTTPSConnection("api.collectapi.com")

    headers = {
    'content-type': "application/json",
    'authorization': "apikey ENTER YOUR API KEY HERE"
    }
    conn.request("GET", "/corona/coronaNews", headers=headers)
    res = conn.getresponse()
    res = res.read()
    res = json.loads(res)
    res = res['result']
    return res

@app.route("/information/countrybyname/<string:country>")
def countryByName(country):
    import http.client
    import json
    conn = http.client.HTTPSConnection("api.collectapi.com")
    headers = {
    'content-type': "application/json",
    'authorization': "apikey ENTER YOUR API KEY HERE"
     }
    
    conn.request("GET","/corona/countriesData?country="+country ,headers=headers)
    res = conn.getresponse()
    data = res.read()
    return data

if __name__=="__main__":
    app.run(debug=True)
