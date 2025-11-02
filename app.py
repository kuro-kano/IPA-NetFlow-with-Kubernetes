from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
mydb = client["mydatabase"]
mycol = mydb["mycollection"]

app = Flask(__name__)


@app.route("/")
def main():
    return render_template("index.html", mycol=mycol)


@app.route("/add", methods=["POST"])
def add_comment():
    ip = request.form.get("ip")
    username = request.form.get("username")
    password = request.form.get("password")
    if ip and username and password:
        mycol.insert_one({"ip": ip, "username": username, "password": password})
    return redirect(url_for("main"))


@app.route("/delete", methods=["POST"])
def delete_comment():
    try:
        idx = int(request.form.get("idx"))
        routers = list(mycol.find())
        if 0 <= idx < len(routers):
            mycol.delete_one({"_id": routers[idx]["_id"]})
    except Exception:
        pass
    return redirect(url_for("main"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
