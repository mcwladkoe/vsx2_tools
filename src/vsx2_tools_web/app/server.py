import sys
import argparse

from flask_babel import _, get_locale

from flask import (
    request,
    render_template,
    json,
    redirect,
    make_response,
    url_for,
)
from waitress import serve

from vsx2_change_layout import change_layout, get_all_layouts
from vsx2_rotate import get_rotated_string, ROTATE_MAP

from . import app


@app.route('/')
@app.route('/index')
def index():
    return render_template(
        "index.html",
        locale=get_locale()
    )


@app.route('/layout', methods=["get", "post"])
def layout():
    input_str = request.values.get('i') or ''
    source = request.values.get('source')
    destination = request.values.get('destination')
    if not input_str and request.method == 'POST':
        return app.response_class(
            status=400,
        )
    if input_str and len(input_str) > 10000 and request.method == 'POST':
        return app.response_class(
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
        return app.response_class(
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


@app.route('/strikethrough', methods=["get", "post"])
def strikethrough():
    input_str = request.values.get('i') or ''
    if not input_str and request.method == 'POST':
        return app.response_class(
            status=400,
        )
    if input_str and len(input_str) > 10000 and request.method == 'POST':
        return app.response_class(
            status=400,
            response=_("textTooLong")
        )
    result_str = ''
    if input_str:
        result_str = ''
        for i in input_str:
            result_str += i + '\u0336'
    if request.method == 'POST':
        return app.response_class(
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


@app.route('/rotate', methods=["get", "post"])
def rotate():
    input_str = request.values.get('i') or ''
    if not input_str and request.method == 'POST':
        return app.response_class(
            status=400,
        )
    if input_str and len(input_str) > 10000 and request.method == 'POST':
        return app.response_class(
            status=400,
            response=_("textTooLong")
        )
    result_str = ''
    if input_str:
        result_str = get_rotated_string(input_str)
    if request.method == 'POST':
        return app.response_class(
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


@app.route('/rotate/doc', methods=["get"])
def rotate_doc():
    return render_template(
        "rotate_doc.html",
        page_title=_('rotateDocPageTitle'),
        mapping=ROTATE_MAP,
        locale=get_locale()
    )


@app.route('/setlang', methods=["get"])
def setlang():
    referrer = request.referrer or url_for('index')
    resp = make_response(redirect(referrer, code=302))
    resp.set_cookie('locale', request.values.get('locale'))
    return resp


def main(argv=sys.argv):
    description = """
        Start server.
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '-s',
        '--host',
        dest='host',
        help='Host',
        default='0.0.0.0'
    )

    parser.add_argument(
        '-p',
        '--port',
        dest='port',
        default=8080,
        type=int,
        help='Port'
    )

    args = parser.parse_args(argv[1:])

    serve(app, host=args.host, port=args.port)
