from flask import Flask,redirect,url_for,render_template,flash, request, jsonify
from flask_mysqldb import MySQL

from dotenv import load_dotenv
load_dotenv()
from create import create
from edit import edit
from delete import delete
import cloudinary
import cloudinary.uploader
import MySQLdb
import os

app = Flask(__name__)
app.register_blueprint(create,url_prefix="/create")
app.register_blueprint(edit,url_prefix="/edit")
app.register_blueprint(delete,url_prefix="/delete")
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
    ##get student data
    stud_cur = mysql.connection.cursor()
    stud_query = "SELECT * FROM student"
    stud_cur.execute(stud_query)
    stud_data = stud_cur.fetchall()
    stud_cur.close()
    ##end of getting the student data
    ##get college data
    coll_cur = mysql.connection.cursor()
    coll_query = "SELECT * FROM college"
    coll_cur.execute(coll_query)
    coll_data = coll_cur.fetchall()
    coll_cur.close()
    ## end of getting the college data
    ##get course data
    course_cur = mysql.connection.cursor()
    course_query = "SELECT * FROM course"
    course_cur.execute(course_query)
    course_data = course_cur.fetchall()
    course_cur.close()
    return render_template("index.html",stud_data = stud_data,coll_data = coll_data, course_data = course_data)




if __name__ == "__main__":
    app.run()