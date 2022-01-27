from flask import Blueprint,Flask,redirect,url_for,render_template,flash, request, jsonify
from flask_mysqldb import MySQL
from datetime import date
import MySQLdb
import cloudinary
import cloudinary.uploader
college = Blueprint("college",__name__,template_folder="templates")
app = Flask(__name__)
mysql = MySQL(app)

@college.route("/edit/college/<value>", methods=["POST","GET"])
def edit(value):
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

@college.route("/delete/college/<value>")
def delete(value):
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

@college.route('/create/college/', methods=["POST","GET"])
def create():
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
                return redirect(url_for("college.create"))
            
        except MySQLdb.IntegrityError:
            flash("Failed to create college")
            return redirect(url_for("college.create"))
        except:
            flash("Failed to create college")
            return redirect(url_for("college.create"))
        
    else:
        return render_template("/create/college.html")
    return render_template("/create/college.html")