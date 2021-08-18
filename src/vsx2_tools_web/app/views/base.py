from flask import request, render_template, Blueprint, redirect, make_response, url_for

base = Blueprint("base", __name__, url_prefix="")


@base.route("/")
@base.route("/index")
def index():
    return render_template("index.html")


@base.route("/setlang", methods=["get"])
def setlang():
    referrer = request.referrer or url_for("base.index")
    resp = make_response(redirect(referrer, code=302))
    resp.set_cookie("locale", request.values.get("locale"))
    return resp
