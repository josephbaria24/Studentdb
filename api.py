from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "studentdb"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data


@app.route("/students", methods=["GET"])
def get_students():
    data = data_fetch("""select * from students""")
    return make_response(jsonify(data), 200)


@app.route("/students/<int:ID>", methods=["GET"])
def get_students_by(ID):
    data = data_fetch("""SELECT * FROM students where students_ID = {}""".format(ID))
    return make_response(jsonify(data), 200)


@app.route("/students/<int:ID>/seat", methods=["GET"])
def get_seat_by_students(ID):
    data = data_fetch(
        """
        SELECT students.FirstNAme, students.LastName, seat.seat_position, seat.seat_no
from students
inner join seat
on students.ID = seat.ID
where students.ID = {}
    """.format(
            ID
        )
    )
    return make_response(
        jsonify({"students_ID": ID, "count": len(data), "seat": data}), 200
    )

@app.route("/students/<int:ID>/course", methods=["GET"])
def get_course_by_students(ID):
    data = data_fetch(
        """
        SELECT students.FirstNAme, students.LastName, course.Course_name, course.Course_ID
from students
inner join course
on students.ID = course.ID
where students.ID = {}
    """.format(
            ID
        )
    )
    return make_response(
        jsonify({"students_ID": ID, "count": len(data), "course": data}), 200
    )





@app.route("/students", methods=["POST"])
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
        jsonify(
            {"message": "students added successfully", "rows_affected": rows_affected}
        ),
        201,
    )


@app.route("/students/<int:ID>", methods=["PUT"])
def update_students(ID):
    cur = mysql.connection.cursor()
    info = request.get_json()
    first_name = info["first_name"]
    last_name = info["last_name"]
    cur.execute(
        """ UPDATE actor SET first_name = %s, last_name = %s WHERE ID = %s """,
        (FirstNAme, LastName, ID),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "actor updated successfully", "rows_affected": rows_affected}
        ),
        200,
    )


@app.route("/students/<int:ID>", methods=["DELETE"])
def delete_students(ID):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM students where ID = %s """, (ID,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "students deleted successfully", "rows_affected": rows_affected}
        ),
        200,
    )

@app.route("/students/format", methods=["GET"])
def get_params():
    fmt = request.args.get('ID')
    foo = request.args.get('aaaa')
    return make_response(jsonify({"format":fmt, "foo":foo}),200)

if __name__ == "__main__":
    app.run(debug=True)
