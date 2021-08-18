import json

from flask_babel import _

from flask import render_template, Blueprint, Response

from ..models.forms import StrikethroughForm

strikethrough = Blueprint("strikethrough", __name__, url_prefix="/strikethrough")


@strikethrough.route("/", methods=["get", "post"])
def index():
    form = StrikethroughForm(meta={"csrf": False})
    if form.validate_on_submit():
        result_str = ""
        for i in form.input_.data:
            result_str += i + "\u0336"
        return Response(
            response=json.dumps(
                {
                    "result": result_str,
                }
            ),
            status=200,
            mimetype="application/json",
        )
    # TODO: return response with validation error
    return render_template(
        "strikethrough.html", page_title=_("strikethroughPageTitle"), form=form
    )
