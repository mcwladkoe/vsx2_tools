from flask import Flask, request

from flask_babel import Babel
from flask_assets import Environment, Bundle

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

css = Bundle(
    'bootstrap/css/bootstrap.css',
    'styles.css',
    filters='cssmin',
    output='gen/site.css'
)
assets.register('css_all', css)


@babel.localeselector
def get_locale():
    locale = request.cookies.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])
