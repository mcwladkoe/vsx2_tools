from flask_babel import _, get_locale

from flask import request, render_template, json, Blueprint, Response

from vsx2_rotate import get_rotated_string, ROTATE_MAP

rotator = Blueprint('rotator', __name__, url_prefix='/rotate')


@rotator.route('/', methods=["get", "post"])
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
        result_str = get_rotated_string(input_str)
    if request.method == 'POST':
        return Response(
            response=json.dumps({
                "result": result_str,
            }),
            status=200,
            mimetype='application/json'
        )
    return render_template(
        "rotate.html",
        page_title=_('rotatePageTitle'),
        locale=get_locale(),
        input_str=input_str,
        result_str=result_str
    )


@rotator.route('/doc', methods=["get"])
def doc():
    return render_template(
        "rotate_doc.html",
        page_title=_('rotateDocPageTitle'),
        mapping=ROTATE_MAP,
        locale=get_locale()
    )
