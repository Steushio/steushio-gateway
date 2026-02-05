#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tempfile
from flask import Flask, send_file, render_template
from MyQR import myqr

app = Flask(__name__, template_folder='views')
app.secret_key = os.environ.get("SECRET", "steushio-secret")


def safe_filename(text):
    return text.replace("@", "_").replace(".", "_")


@app.route("/css")
def serve_css():
    return send_file("static/css/style.css", mimetype="text/css")


@app.route("/qr/<id>/<amount>")
def serve_qr(id, amount):
    return send_file(create_qr(id, amount), mimetype="image/png")


def create_qr(id, amount):
    upi_id = id
    save_dir = tempfile.gettempdir()

    try:
        amount = float(amount)
    except Exception:
        amount = 0

    if amount > 0:
        url = f"upi://pay?pn=STEUSHIO&pa={upi_id}&cu=INR&am={amount}"
    else:
        url = f"upi://pay?pn=STEUSHIO&pa={upi_id}&cu=INR"

    filename = f"{safe_filename(upi_id)}_qr.png"

    myqr.run(
        url,
        level="H",
        colorized=False,
        save_name=filename,
        save_dir=save_dir
    )

    return f"{save_dir}/{filename}"


@app.route("/")
def homepage():
    return render_template("create.html")


@app.route("/<id>")
def payment(id):
    if "@" in id:
        return render_template("home.html", id=id, amount=0)
    return render_template("create.html")


@app.route("/<id>/<amount>")
def amount_payment(id, amount):
    if "@" in id:
        return render_template("home.html", id=id, amount=amount)
    return render_template("create.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
