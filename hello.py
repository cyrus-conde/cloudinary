from flask import Flask,redirect,url_for,render_template,flash, request, jsonify
from flask_mysqldb import MySQL

from dotenv import load_dotenv
load_dotenv()
from student import student
from course import course
from college import college
import cloudinary
import cloudinary.uploader
import MySQLdb
import os

app = Flask(__name__)
app.register_blueprint(student,url_prefix="/")
app.register_blueprint(course,url_prefix="/")
app.register_blueprint(college,url_prefix="/")
mysql = MySQL(app)

app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PWD")
app.config["MYSQL_DB"] = os.getenv("MYSQL_DB")

app.secret_key = os.getenv("SECRET")


cloudinary.config( 
  cloud_name = os.getenv("cloud_name"), 
  api_key = os.getenv("cloud_api_key"), 
  api_secret = os.getenv("cloud_api_secret") 
)

@app.route("/create/")
def createDashboard():
    return render_template("create.html")


@app.route('/searchField', methods=['GET','POST'])
def searchField():
    
    if request.method == "POST":
        datas=request.form['query']
        table=request.form['table']
        column=request.form['column']
        cur = mysql.connection.cursor()
        
        likestring = "%" + datas + "%"
        if datas == "":
            cur.execute("SELECT * FROM " + table)
            data = cur.fetchall()
        elif table == "":
            data = "NO TABLE SELECTED"
        else:
            cur.execute("SELECT * FROM " + table + " WHERE " + column + " LIKE %s", (likestring,))
            data = cur.fetchall()
        
        #cur.execute("SELECT * FROM student WHERE id LIKE %s", (datas,))
        
        
    return jsonify({'htmlresponse':render_template('response.html', data = data, table=table)})

@app.route('/', methods=["POST","GET"])
def index():
    return render_template("index.html")




if __name__ == "__main__":
    app.run()