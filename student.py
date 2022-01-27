from flask import Blueprint,Flask,redirect,url_for,render_template,flash, request, jsonify
from flask_mysqldb import MySQL
from datetime import date
import MySQLdb
import cloudinary
import cloudinary.uploader
student = Blueprint("student",__name__,template_folder="templates")
app = Flask(__name__)
mysql = MySQL(app)
ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg", "gif"]

idnum = ""
nnnn = 1

#generate ID Number
def set_idnum(number):
    global idnum
    global nnnn
    todays_date = date.today()
    number = number
    nnnn = '{0:04}'.format(number)
    curr_year = todays_date.year
    IDNumber = str(curr_year) + "-" + str(nnnn)
    new_number = IDNumber.split("-")
    new_number = '{0:01}'.format(int(new_number[1]))
    new_number = int(new_number) + 1
    idnum = IDNumber
    nnnn = new_number

def get_idnum():
    return idnum

def set_nnnn():
    global nnnn
    cur = mysql.connection.cursor()
    query = "SELECT `id` FROM `student` ORDER BY id DESC LIMIT 1"
    if cur.execute(query):
        data = cur.fetchall()
        cur.close()
        for rows in data: 
            nnnn = rows[0]
        nnnn = nnnn.split("-")
        nnnn = '{0:01}'.format(int(nnnn[1]))
        nnnn = int(nnnn) + 1
    else:
        nnnn = 1
def get_nnnn():
    return nnnn

@student.route("/delete/student/<value>")
def delete(value):
    try:
        delete = mysql.connection.cursor()
        del_query = "DELETE FROM student WHERE id = %s"
        del_values = (value,)
        
        delete.execute(del_query,del_values)
        mysql.connection.commit()
        delete.close()
        flash("Student has been deleted")
        return redirect(url_for('index'))
    except:
        flash("Failed to delete student")
        return redirect(url_for("index"))

@student.route("/edit/student/<value>",methods=["POST","GET"])
def edit(value):
    if request.method == "POST":
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        course = request.form['course']
        yearLevel = request.form['yearLevel']
        gender = request.form['gender']
        #image = request.files['image']
        cur = mysql.connection.cursor()
        edit_stud_que = "UPDATE student SET firstname=%s,lastname=%s,course=%s,yearLevel=%s,gender=%s WHERE id = %s"
        #if image and image.filename.split(".")[-1].lower() in ALLOWED_EXTENSIONS:
            #image_url = cloudinary.uploader.upload(image)
            #image_url['secure_url'],
        edit_stud_val = (firstname,lastname,course,yearLevel,gender,value)
        try:
            if cur.execute(edit_stud_que,edit_stud_val):
                mysql.connection.commit()
                cur.close()
                flash("Student has been updated")
            return redirect(url_for("index"))
        except:
            flash("Failed to update student")
            return redirect(url_for("index"))    

    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM student WHERE id = %s", (value,))
        data = cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT code FROM course")
        coursedata = cur.fetchall()
        cur.close()
        if data:
            return render_template("/edit/student.html", results=data,coursedata=coursedata)
        else:
            return "No Data Found"


@student.route('/create/student/', methods=["POST","GET"])
def create():
    
    if request.method == "POST":
        set_nnnn()
        nnnn = get_nnnn()
        set_idnum(nnnn)
        IDNumber = get_idnum()
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        course = request.form['course']
        yearLevel = request.form['yearLevel']
        gender = request.form['gender']
        image = request.files['image']
        cur = mysql.connection.cursor()
        query = "INSERT INTO `student`(`id`,`firstname`,`lastname`,`course`,`yearLevel`,`gender`,`image_url`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        
        if image and image.filename.split(".")[-1].lower() in ALLOWED_EXTENSIONS:
            image_url = cloudinary.uploader.upload(image)
            values = (IDNumber,firstname,lastname,course,yearLevel,gender,image_url["secure_url"])
            try:
                if cur.execute(query,values):
                    mysql.connection.commit()
                    cur.close()
                    flash("Student successfully created")
                    return redirect(url_for("student.create"))
            except MySQLdb.IntegrityError:
                flash("Failed to create student")
                return redirect(url_for("student.create"))
            except:
                flash("Failed to create student")
                return redirect(url_for("student.create"))
    else:
        cur = mysql.connection.cursor()
        query = "SELECT code FROM course"
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        return render_template("/create/student.html",data = data)
    return render_template("/create/student.html")