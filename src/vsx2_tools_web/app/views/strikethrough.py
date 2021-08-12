import json

from flask_babel import _, get_locale

from flask import render_template, Blueprint, request, Response

strikethrough = Blueprint('strikethrough', __name__, url_prefix='/strikethrough')


@strikethrough.route('/', methods=["get", "post"])
def index():
    input_str = request.values.get('i') or ''
    if not input_str and request.method == 'POST':
        return Response(status=400)
    if input_str and len(input_str) > 10000 and request.method == 'POST':
        return Response(
            status=400,
            response=_("textTooLong")
        )
    result_str = ''
    if input_str:
        result_str = ''
        for i in input_str:
            result_str += i + '\u0336'
    if request.method == 'POST':
        return Response(
            response=json.dumps({
                "result": result_str,
            }),
            status=200,
            mimetype='application/json'
        )
    return render_template(
        "strikethrough.html",
        page_title=_('strikethroughPageTitle'),
        locale=get_locale(),
        input_str=input_str,
        result_str=result_str
    )
