from flask_babel import _

from flask import request, render_template, json, Blueprint, Response

from vsx2_rotate import get_rotated_string, ROTATE_MAP
from ..models.forms import RotateForm

rotator = Blueprint("rotator", __name__, url_prefix="/rotate")


@rotator.route("/", methods=["get", "post"])
def index():
    form = RotateForm()
    if form.validate_on_submit():
        result_str = get_rotated_string(form.input_.data)
        return Response(
            response=json.dumps(
                {
                    "result": result_str,
                }
            ),
            status=200,
            mimetype="application/json",
        )
    if request.method == "POST":
        return Response(
            response=json.dumps(
                {
                    "errors": form.errors,
                }
            ),
            status=400,
            mimetype="application/json",
        )

    return render_template("rotate.html", page_title=_("rotatePageTitle"), form=form)


@rotator.route("/doc", methods=["get"])
def doc():
    return render_template(
        "rotate_doc.html", page_title=_("rotateDocPageTitle"), mapping=ROTATE_MAP
    )
