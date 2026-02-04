from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "users.db")


appp = Flask(__name__)
appp.secret_key = "secret123"

ADMIN_USERNAME = "Admin"
ADMIN_PASSWORD = "admin1389"


def create_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT
    )
    """)
    conn.commit()
    conn.close()

create_db()

@appp.route("/")
def home():
    return render_template("index.html")

@appp.route("/register",methods=["GET","POST"])
def register():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("INSERT INTO users(username,password) VALUES (?,?)",(user,pwd))
        conn.commit()
        conn.close()

        return "sign up complete!"
    return render_template("register.html")

@appp.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        if user == ADMIN_USERNAME and pwd == ADMIN_PASSWORD:
            
            session["Admin"] = True
            return redirect("/admin_dashboard")
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?",(user,pwd))
        result = cur.fetchone()
        conn.close()

        if result:
            session["user"] = user
            return redirect("/dashboard")
        else:
            return "information is incorrect !"
    return render_template("login.html")

@appp.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template("dashboard.html",username=session["user"])
    else:
        return redirect("/login")
    
@appp.route("/logout")
def logout():
    session.pop("user",None)
    return redirect("/")

@appp.route("/admin_dashboard")
def admin_dashboard():
    if "Admin"  not in session:
        return redirect("/login")
    return render_template("admin_dashboard.html")
    
@appp.route("/delete/<int:user_id>")
def delete_user(user_id):
    if "Admin" not in session:
        return redirect("/login")
    else:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id=?",(user_id,))
        conn.commit()
        conn.close()
        return redirect("/admin")

@appp.route("/admin")
def admin():
    if "Admin" not in session:
        return redirect("/login")
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    conn.close()
    return render_template("admin.html",users=users)


if __name__ == "__main__":
    appp.run(host="0.0.0.0",port=10000)