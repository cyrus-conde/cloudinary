from flask import Blueprint,Flask,redirect,url_for,render_template,flash, request, jsonify
from flask_mysqldb import MySQL
from datetime import date
import MySQLdb
import cloudinary
import cloudinary.uploader
course = Blueprint("course",__name__,template_folder="templates")
app = Flask(__name__)
mysql = MySQL(app)

@course.route("/delete/course/<value>")
def delete(value):
    try:
        delete = mysql.connection.cursor()
        del_query = "DELETE FROM course WHERE code = %s"
        del_values = (value,)
        delete.execute(del_query,del_values)
        mysql.connection.commit()
        delete.close()
        flash("Course has been deleted")
        return redirect(url_for('index'))
    except:
        flash("Failed to delete course")
        return redirect(url_for("index"))

@course.route("/edit/course/<value>", methods=["POST", "GET"])
def edit(value):
    if request.method == "POST":
        courseCode = request.form['course-code']
        courseName = request.form['course-name']
        collegeCode = request.form['college-code']
        try:
            cur = mysql.connection.cursor()
            edit_course_que = "UPDATE course SET name = %s, college = %s, code = %s WHERE code = %s"
            edit_course_val = (courseName,collegeCode,courseCode,value)
            cur.execute(edit_course_que,edit_course_val)
            mysql.connection.commit()
            cur.close()
            flash("Course has been updated")
            return redirect(url_for("index"))
        except:
            flash("Failed to update course")
            return redirect(url_for("index"))

    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM course WHERE code = %s", (value,))
        data = cur.fetchall()
        cur.close()
        cur = mysql.connection.cursor()
        cur.execute("SELECT code FROM college")
        collegedata = cur.fetchall()
        cur.close()
        if data:
            return render_template("/edit/course.html", results=data,collegedata=collegedata)
        else:
            return "No Data Found"

@course.route('/create/course/', methods=["POST","GET"])
def create():
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
                return redirect(url_for("course.create"))
        except MySQLdb.IntegrityError:
            flash("Failed to create course")
            return redirect(url_for("course.create"))
        except:
            flash("Failed to create course")
            return redirect(url_for("course.create"))
    else:
        cur = mysql.connection.cursor()
        query = "SELECT code FROM college"
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        return render_template("/create/course.html",data=data)
    return render_template("/create/course.html")