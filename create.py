from flask import Blueprint,Flask,redirect,url_for,render_template,flash, request, jsonify
from flask_mysqldb import MySQL
from datetime import date
import MySQLdb
import cloudinary
import cloudinary.uploader
create = Blueprint("create",__name__,template_folder="templates")
app = Flask(__name__)
mysql = MySQL(app)
ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg", "gif"]
@create.route("/")
def createDashboard():
    return render_template("create.html")
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
@create.route('/college/', methods=["POST","GET"])
def create_college():
    if request.method == "POST":
        collegeCode = request.form['college-code']
        collegeName = request.form['college-name']
        cur = mysql.connection.cursor()
        query = "INSERT INTO `college`(`code`,`name`) VALUES (%s,%s)"
        values = (collegeCode,collegeName)
        try:
            if cur.execute(query, values):
                mysql.connection.commit()
                cur.close()
                flash("College successfully created")
                return redirect(url_for("create.create_college"))
            
        except MySQLdb.IntegrityError:
            flash("Failed to create college")
            return redirect(url_for("create.create_college"))
        except:
            flash("Failed to create college")
            return redirect(url_for("create.create_college"))
        
    else:
        return render_template("/create/college.html")
    return render_template("/create/college.html")

@create.route('/course/', methods=["POST","GET"])
def create_course():
    if request.method == "POST":
        courseCode = request.form['course-code']
        courseName = request.form['course-name']
        collegeCode = request.form['college-code']
        cur = mysql.connection.cursor()
        query = "INSERT INTO `course`(`code`,`name`,`college`) VALUES (%s,%s,%s)"
        values = (courseCode,courseName,collegeCode)
        try:         
            if cur.execute(query, values):
                mysql.connection.commit()
                cur.close()
                flash("Course successfully created")
                return redirect(url_for("create.create_course"))
        except MySQLdb.IntegrityError:
            flash("Failed to create course")
            return redirect(url_for("create.create_course"))
        except:
            flash("Failed to create course")
            return redirect(url_for("create.create_course"))
    else:
        cur = mysql.connection.cursor()
        query = "SELECT code FROM college"
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        return render_template("/create/course.html",data=data)
    return render_template("/create/course.html")

@create.route('/student/', methods=["POST","GET"])
def create_student():
    
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
                    return redirect(url_for("create.create_student"))
            except MySQLdb.IntegrityError:
                flash("Failed to create student")
                return redirect(url_for("create.create_student"))
            except:
                flash("Failed to create student")
                return redirect(url_for("create.create_student"))
    else:
        cur = mysql.connection.cursor()
        query = "SELECT code FROM course"
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        return render_template("/create/student.html",data = data)
    return render_template("/create/student.html")