from flask_babel import _, get_locale

from flask import render_template, Blueprint

role_formatter = Blueprint('role_formatter', __name__, url_prefix='/role_formatter')


@role_formatter.route('/', methods=["get"])
def index():
    return render_template(
        "role_formatter.html",
        page_title=_('roleFormatterPageTitle'),
        locale=get_locale(),
    )
