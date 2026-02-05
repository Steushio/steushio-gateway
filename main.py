#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tempfile
from flask import Flask, send_file, render_template
from MyQR import myqr

app = Flask(__name__, template_folder='views', static_folder='/tmp/')

# Optional secret (not required for functionality)
app.secret = os.environ.get('SECRET')


@app.route('/css')
def serve_css():
    # Serve CSS explicitly (same as original behavior)
    return send_file('static/css/style.css', mimetype='text/css')


@app.route('/qr/<id>/<amount>')
def serve_qr(id, amount):
    return send_file(create_qr(id, amount), mimetype='image/png')


def create_qr(id, amount=None):
    upi_id = id
    save_dir = tempfile.gettempdir()

    # Build UPI intent
    if amount:
        try:
            amount = round(float(amount), 2)
            url = f"upi://pay?pn=STEUSHIO&pa={upi_id}&cu=INR&am={amount}"
        except Exception:
            url = f"upi://pay?pn=STEUSHIO&pa={upi_id}&cu=INR"
    else:
        url = f"upi://pay?pn=STEUSHIO&pa={upi_id}&cu=INR"

    # Generate QR (no logo, clean QR)
    myqr.run(
        url,
        version=1,
        level='H',
        colorized=False,
        save_name=f"{upi_id}_qr.png",
        save_dir=save_dir
    )

    return f"{save_dir}/{upi_id}_qr.png"


@app.route('/')
def homepage():
    return render_template('create.html')


@app.route('/<id>')
def payment(id):
    if '@' in id:
        return render_template('home.html', id=id, amount=None)
    return render_template('create.html')


@app.route('/<id>/<amount>')
def amount_payment(id, amount):
    if '@' in id:
        try:
            amount = round(float(amount), 2)
        except Exception:
            amount = None
        return render_template('home.html', id=id, amount=amount)
    return render_template('create.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, use_reloader=True)

