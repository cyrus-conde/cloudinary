from flask import Blueprint,Flask,redirect,url_for,render_template,flash, request, jsonify
from flask_mysqldb import MySQL
import MySQLdb
import os
import cloudinary
import cloudinary.uploader
edit = Blueprint("edit",__name__,template_folder="templates")
app = Flask(__name__)
mysql = MySQL(app)


@edit.route("/course/<value>", methods=["POST", "GET"])
def course(value):
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

@edit.route("/college/<value>", methods=["POST","GET"])
def college(value):
    if request.method == "POST":
        collegeCode = request.form['college-code']
        collegeName = request.form['college-name']
        try:
            cur = mysql.connection.cursor()
            edit_coll_que = "UPDATE college SET code = %s, name = %s WHERE code = %s"
            edit_coll_val = (collegeCode,collegeName,value)
            cur.execute(edit_coll_que,edit_coll_val)
            mysql.connection.commit()
            cur.close()
            flash("College has been updated")
            return redirect(url_for("index"))
        except:
            flash("Failed to update college")
            return redirect(url_for("index"))

    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM college WHERE code = %s", (value,))
        data = cur.fetchall()
        cur.close()
        if data:
            return render_template("/edit/college.html", results=data)
        else:
            return "No Data Found"

@edit.route("/student/<value>",methods=["POST","GET"])
def student(value):
    if request.method == "POST":
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        course = request.form['course']
        yearLevel = request.form['yearLevel']
        gender = request.form['gender']
        image = request.files['image']
        cur = mysql.connection.cursor()
        edit_stud_que = "UPDATE student SET firstname=%s,lastname=%s,course=%s,yearLevel=%s,gender=%s,image_url=%s WHERE id = %s"
        if image and image.filename.split(".")[-1].lower() in ALLOWED_EXTENSIONS:
            image_url = cloudinary.uploader.upload(image)
            edit_stud_val = (firstname,lastname,course,yearLevel,gender,image_url['secure_url'],value)
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

