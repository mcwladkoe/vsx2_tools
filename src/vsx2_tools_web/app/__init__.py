from flask import Flask, request

from flask_babel import Babel
from flask_assets import Environment, Bundle

from .views.base import base
from .views.role_formatter import role_formatter
from .views.strikethrough import strikethrough
from .views.meme_generator import meme_generator
from .views.rotate import rotator
from .views.layout import layout
from ..config import Config


app = Flask(
    __name__,
    static_url_path='/static'
)

app.config.from_object(Config)
babel = Babel(app)

assets = Environment(app)

js = Bundle(
    'jquery.min.js',
    'bootstrap/js/bootstrap.js',
    'popper.js',
    'bootstrap-notify.min.js',
    'main.js',
    filters='jsmin',
    output='gen/site.js'
)
assets.register('js_all', js)

vue = Bundle(
    'js/vue.js',
    'js/vue-app.js',
    filters='jsmin',
    output='gen/app.js'
)
assets.register('js_vue', vue)

css = Bundle(
    'bootstrap/css/bootstrap.css',
    'styles.css',
    filters='cssmin',
    output='gen/site.css'
)
assets.register('css_all', css)

app.register_blueprint(base)
app.register_blueprint(meme_generator)
app.register_blueprint(rotator)
app.register_blueprint(layout)
app.register_blueprint(role_formatter)
app.register_blueprint(strikethrough)


@babel.localeselector
def get_locale():
    locale = request.cookies.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])
