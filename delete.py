from flask import Blueprint,Flask,redirect,url_for,render_template,flash, request, jsonify
from flask_mysqldb import MySQL
import MySQLdb
import os
delete = Blueprint("delete",__name__,template_folder="templates")
app = Flask(__name__)
mysql = MySQL(app)

@delete.route("/student/<value>")
def student(value):
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

@delete.route("/college/<value>")
def college(value):
    try:
        delete = mysql.connection.cursor()
        del_query = "DELETE FROM college WHERE code = %s"
        del_values = (value,)
        delete.execute(del_query,del_values)
        mysql.connection.commit()
        delete.close()
        flash("College has been deleted")
        return redirect(url_for('index'))
    except:
        flash("Failed to delete college")
        return redirect(url_for("index"))

@delete.route("/course/<value>")
def course(value):
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