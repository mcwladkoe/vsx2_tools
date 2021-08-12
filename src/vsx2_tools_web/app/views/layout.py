from flask_babel import _, get_locale

from flask import request, render_template, json, Blueprint, Response

from vsx2_change_layout import change_layout, get_all_layouts

layout = Blueprint('layout', __name__, url_prefix='/layout')


@layout.route('/', methods=["get", "post"])
def index():
    input_str = request.values.get('i') or ''
    source = request.values.get('source')
    destination = request.values.get('destination')
    if not input_str and request.method == 'POST':
        return Response(status=400)
    if input_str and len(input_str) > 10000 and request.method == 'POST':
        return Response(
            status=400,
            response=_("textTooLong")
        )
    result_str = ''
    if input_str or source or destination:
        result_str = change_layout(
            source_str=input_str,
            source_layout=source,
            destination_layout=destination
        )
    if request.method == 'POST':
        return Response(
            response=json.dumps({
                "result": result_str,
            }),
            status=200,
            mimetype='application/json'
        )
    return render_template(
        "layout.html",
        page_title=_('layoutPageTitle'),
        layouts=get_all_layouts(),
        locale=get_locale(),
        input_str=input_str,
        source=source,
        destination=destination,
        result_str=result_str
    )
