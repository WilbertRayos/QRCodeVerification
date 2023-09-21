from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import Users, SSLSES, CSSR
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint("auth", __name__)

@auth.route("/admin/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            user = Users.query.filter_by(email=email).first()

            if user:
                if check_password_hash(user.passwd, password):
                    login_user(user, remember=True)
                    flash("Welcome!", category="success")
                    return redirect(url_for("views.sslses"))
            else:
                flash("Invalid User", category="error")
        return render_template("login.html", user=current_user)
    else:
        return render_template("login.html", user=current_user)

@auth.route("/", methods=['GET', 'POST'])
def home():
    return "<h1>Welcome to NTC</h1>"

@auth.route("/logout")
@login_required
def logout():
    try:
        logout_user()
    except Exception as e:
        flash("Invalid User", category="error")
    return redirect(url_for("auth.login"))

@auth.route("/delete_sslses/<id>", methods=["GET"])
@login_required
def delete_sslses_entry(id):
    try:
        entry = SSLSES.query.filter_by(id=id).first()
        db.session.delete(entry)
        db.session.commit()
        flash("Entry has been deleted successfully", category="success")
    except Exception as e:
        flash("Delete operation could not perform", category="error")
    return redirect(url_for("views.sslses_list"))

@auth.route("/delete_cssr/<id>", methods=["GET"])
@login_required
def delete_cssr_entry(id):
    try:
        entry = CSSR.query.filter_by(id=id).first()
        db.session.delete(entry)
        db.session.commit()
        flash("Entry has been deleted successfully", category="success")
    except Exception as e:
        flash("Delete operation could not perform", category="error")

    return redirect(url_for("views.cssr_list"))