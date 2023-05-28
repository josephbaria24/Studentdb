from flask import Flask, make_response, request, jsonify
import functools
from flask_mysqldb import MySQL
import xml.etree.ElementTree as ET
import xmltodict

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "studentdb"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == "admin" and auth.password == "admin":
            return f(*args, **kwargs)
        return make_response('Could not verify your login!',401,{'WWW-Authenticate':'Basic realm="Login Required"'})
    return decorated_function 



mysql = MySQL(app)


@app.route("/")
@login_required
def hello_world():
    return "<p>STUDENT DATABASE</p>"


def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data




@app.route("/students", methods=["GET"])
@login_required
def get_students():
    firstname = request.args.get("firstname")
    lastname = request.args.get("lastname")
    address = request.args.get("address")
    formatparam = request.args.get("format")
    quer = "SELECT * FROM students WHERE 1=1"
    if firstname:
        quer += f" AND FirstNAme LIKE '{firstname}%'"
    if lastname:
        quer += f" AND LastName LIKE '{lastname}%'"
    if address:
        quer += f" AND Address LIKE '{address}%'"
        
    if formatparam and formatparam.lower() == 'xml':
        data = data_fetch(quer)
        xml_data = xmltodict.unparse({"students": {"student": data}})
        response = make_response(xml_data)
        response.headers["Content-Type"] = "application/xml"
        return response
    else:
        data = data_fetch(quer)
        return make_response(jsonify(data), 200)





@app.route("/students/<int:ID>", methods=["GET"])
@login_required
def get_students_by(ID):
    format_param = request.args.get("format")
    if format_param and format_param.lower() == "xml":
        data = data_fetch("""SELECT * FROM students where ID = {}""".format(ID))
        xml_data = xmltodict.unparse({"students": {"student": data}})
        response = make_response(xml_data)
        response.headers["Content-Type"] = "application/xml"
        return response
    else:
        data = data_fetch("""SELECT * FROM students where ID = {}""".format(ID))
        return make_response(jsonify(data), 200)



@app.route("/students/<int:ID>/seat", methods=["GET"])
@login_required
def get_seat_by_students(ID):
    format_param = request.args.get("format")
    if format_param and format_param.lower() == "xml":
        data = data_fetch(
            """
            SELECT students.FirstNAme, students.LastName, seat.seat_position, seat.seat_no
            from students
            inner join seat
            on students.ID = seat.ID
            where students.ID = {}
            """.format(ID)
        )
        xml_data = xmltodict.unparse({"students":{"student":data}}, pretty=True)
        response = make_response(xml_data)
        response.headers["Content-Type"] = "application/xml"
        return response
    else:
        data = data_fetch(
            """
            SELECT students.FirstNAme, students.LastName, seat.seat_position, seat.seat_no
            from students
            inner join seat
            on students.ID = seat.ID
            where students.ID = {}
            """.format(ID)
        )
        return make_response(jsonify(data), 200)



@app.route("/students/<int:ID>/course", methods=["GET"])
@login_required
def get_course_by_students(ID):
    format_param = request.args.get("format")
    if format_param and format_param.lower() == "xml":
        data = data_fetch(
            """
            SELECT students.FirstNAme, students.LastName, course.Course_name, course.Course_ID
            from students
            inner join course
            on students.ID = course.ID
            where students.ID = {}
            """.format(ID)
        )
        xml_data = xmltodict.unparse({"students":{"student":data}})
        response = make_response(xml_data)
        response.headers["Content-Type"] = "application/xml"
        return response
    else:
        data = data_fetch(
            """
            SELECT students.FirstNAme, students.LastName, course.Course_name, course.Course_ID
            from students
            inner join course
            on students.ID = course.ID
            where students.ID = {}
            """.format(ID)
        )
        return make_response(jsonify(data), 200)



#post

@app.route("/students", methods=["POST"])
@login_required
def add_students():
    cur = mysql.connection.cursor()
    info = request.get_json()
    FirstNAme = info["FirstNAme"]
    LastName = info["LastName"]
    Address = info["Address"]
    cur.execute(
        """ INSERT INTO students (FirstNAme, LastName, Address) VALUE (%s, %s, %s)""",
        (FirstNAme, LastName, Address),
    )
     
    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify({"message": "students added successfully", "rows_affected": rows_affected}),201,)



@app.route("/students/<int:ID>", methods=["PUT"])
@login_required
def update_students(ID):
    cur = mysql.connection.cursor()
    info = request.get_json()
    FirstNAme = info["FirstNAme"]
    LastName = info["LastName"]
    Address = info["Address"]
    cur.execute(
        """ UPDATE students SET FirstNAme = %s, LastName = %s, Address = %s WHERE ID = %s """,
        (FirstNAme, LastName, Address, ID),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(jsonify({"message": "student updated successfully", "rows_affected": rows_affected}),200,)


@app.route("/students/<int:ID>", methods=["DELETE"])
@login_required
def delete_students(ID):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM students where ID = %s """, (ID,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(jsonify({"message": "students deleted successfully", "rows_affected": rows_affected}),200,)


if __name__ == "__main__":
    app.run(debug=True)
