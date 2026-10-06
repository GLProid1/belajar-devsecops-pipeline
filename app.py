"""Modul backend autentikasi Flask dengan antarmuka web interaktif."""

import sqlite3
import datetime
from zoneinfo import ZoneInfo
from flask import Flask, render_template, request

app = Flask(__name__)

def init_db():
    """Inisialisasi basis data dan membuat data pengguna awal."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO users VALUES ('admin', 'supersecret')"
    )
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    """Menampilkan formulir login dan memproses autentikasi."""
    message = None
    status_class = None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        # Parameterized query untuk mencegah SQL Injection
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            message = "Login Berhasil! Selamat datang."
            status_class = "success"
        else:
            message = "Login Gagal! Kredensial tidak valid."
            status_class = "danger"

    return render_template(
        "index.html", message=message, status_class=status_class
    )

@app.route("/version", methods=["GET"])
def version():
    """Endpoint untuk menampilkan versi aplikasi."""
    return {"app": "Flask DevSecOps Pipeline", "version": "1.1.0"}

@app.route("/time", methods=["GET"])
def time():
    """Menampilkan waktu server saat ini."""
    now = datetime.datetime.now(ZoneInfo("Asia/Jakarta"))
    return {"server_time": now.isoformat()}

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)  # nosemgrep
