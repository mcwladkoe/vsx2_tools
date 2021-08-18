from flask_babel import _

from flask import request, render_template, json, Blueprint, Response

from vsx2_change_layout import change_layout
from ..models.forms import LayoutForm


layout = Blueprint("layout", __name__, url_prefix="/layout")


@layout.route("/", methods=["get", "post"])
def index():
    form = LayoutForm()
    if form.validate_on_submit():
        result_str = change_layout(
            source_str=form.input_.data,
            source_layout=form.source.data,
            destination_layout=form.destination.data,
        )
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
    return render_template("layout.html", page_title=_("layoutPageTitle"), form=form)
