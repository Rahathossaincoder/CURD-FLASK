from flask import Flask, render_template, request,flash, redirect, url_for
import traceback
import sqlite3
app = Flask(__name__)
dictionary = {}
app.secret_key = '123'


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/", methods=["GET","POST"])
def store_values():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        roll = request.form.get("roll")
        if name == "" or email == "" or roll == "":
            flash("please fill all boxes...")
        else:
            conn = sqlite3.connect("list.db")
            c = conn.cursor()
            c.execute("""CREATE TABLE IF NOT EXISTS listings(
                    roll INTEGER,
                    name TEXT,
                    email TEXT)
                    """)
            flash("Inserted successfully")
            c.execute("INSERT INTO listings (roll, name, email) VALUES (?, ?, ?)", (roll, name, email))
            conn.commit()
            c.close()
            conn.close()
    return render_template("index.html")

@app.route("/viwe")
def view_list():
    conn = sqlite3.connect("list.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS listings(
                roll INTEGER,
                name TEXT,
                email TEXT)""")
    c.execute("SELECT rowid,* FROM listings")  
    messages = c.fetchall()
    print(messages)
    c.close()
    conn.close()
    return render_template("viwe.html", messages=messages)
@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    conn = sqlite3.connect("list.db")
    c = conn.cursor()
    c.execute("DELETE FROM listings WHERE rowid = ?", (id,))
    conn.commit()
    c.close()
    conn.close()
    return redirect(url_for("view_list"))

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    conn = sqlite3.connect("list.db")
    c = conn.cursor()
    
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        roll = request.form.get("roll")

        if name == "" or email == "" or roll == "":
            flash("Please fill all fields!")
        else:
            c.execute("UPDATE listings SET name = ?, email = ?, roll = ? WHERE rowid = ?", (name, email, roll, id))
            conn.commit()
            flash("Updated successfully!")
            return redirect(url_for("view_list"))

    c.close()
    conn.close()
    
    return render_template("update.html")


@app.errorhandler(500)
def internal_error(error):
    print(traceback.format_exc()) 
    return "Internal server error", 500


if __name__ == "__main__":
    app.run(debug=True)