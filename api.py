from flask import Flask, make_response, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "studentdb"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)


@app.route("/")
def hello():
    return "<p>HELLO, WORLD!!!</p>"

@app.route("/students", methods=["GET"])
def get_actors():
    cur = mysql.connection.cursor()
    query="""
    select * from students
    """
    cur.execute(query)
    data = cur.fetchall()
    cur.close()

    return make_response(jsonify(data),200)

if __name__ == "__main__":
    app.run(debug=True)