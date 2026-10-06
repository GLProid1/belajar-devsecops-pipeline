"""Modul backend autentikasi Flask dengan antarmuka web interaktif."""

import os
import sqlite3
from flask import Flask, request, render_template

app = Flask(__name__)

def init_db():
    """Inisialsasi basis data dan membuat data pengguna awal"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password TEXT NOT NULL)"
    )
    admin_password = os.getenv("ADMIN_PASSWORD")

    if not admin_password:
        raise RuntimeError("ADMIN_PASSWORD belum dikonfigurasi")

    cursor.execute(
        "INSERT OR IGNORE INTO users VALUES (?, ?)",
        ("admin", admin_password)
    )
    conn.commit()
    conn.close()

app.route('/', methods=['GET', 'POST'])
def index():
    """Menampilkan halaman login dan memproses autentikasi"""
    message = None
    status_class = None

    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Parameterisasi query untuk mencegah SQL Injection
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            message = "Login Berhasil. Selamat datang, {}!".format(username)
            status_class = "success"
        else:
            message = "Login Gagal. Username atau password salah."
            status_class = "error"

    return render_template(
        'index.html',
        message=message,
        status_class=status_class
    )

if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0", port=5000)
