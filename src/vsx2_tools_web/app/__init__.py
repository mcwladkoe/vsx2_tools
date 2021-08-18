from flask import Flask, request

from flask_babel import Babel, get_locale as babel_get_locale
from flask_assets import Environment, Bundle
from flask_wtf import CSRFProtect

from .views.base import base
from .views.role_formatter import role_formatter
from .views.strikethrough import strikethrough
from .views.meme_generator import meme_generator
from .views.rotate import rotator
from .views.layout import layout
from ..config import Config
from .. import __version__, BUILD_NUMBER


app = Flask(__name__, static_url_path="/static")

app.config.from_object(Config)
babel = Babel(app)

assets = Environment(app)

js = Bundle(
    "jquery.min.js",
    "bootstrap/js/bootstrap.js",
    "popper.js",
    "bootstrap-notify.min.js",
    "main.js",
    filters="jsmin",
    output="gen/site.js",
)
assets.register("js_all", js)

vue = Bundle("js/vue.js", "js/vue-app.js", filters="jsmin", output="gen/app.js")
assets.register("js_vue", vue)

css = Bundle(
    "bootstrap/css/bootstrap.css", "styles.css", filters="cssmin", output="gen/site.css"
)
assets.register("css_all", css)

app.register_blueprint(base)
app.register_blueprint(meme_generator)
app.register_blueprint(rotator)
app.register_blueprint(layout)
app.register_blueprint(role_formatter)
app.register_blueprint(strikethrough)

csrf = CSRFProtect(app)


@app.context_processor
def inject_app_vars():
    return {
        "app_version": __version__,
        "locale": babel_get_locale(),
        "build_number": BUILD_NUMBER,
    }


@babel.localeselector
def get_locale():
    locale = request.cookies.get("locale")
    if locale and locale in app.config["LANGUAGES"]:
        return locale
    return request.accept_languages.best_match(app.config["LANGUAGES"])
