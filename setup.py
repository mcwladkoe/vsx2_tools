from setuptools import setup, find_packages

requires = [
    'flask',
    'flask_babel',
    'Flask-Assets',
    'jsmin',
    'cssmin',
    'waitress',
    'vsx2_change_layout @ git+https://github.com/mcwladkoe/vsx2_change_layout',
    'vsx2_rotate @ git+https://github.com/mcwladkoe/vsx2_rotate',
]

setup(
    name='vsx2_tools_web',
    version='1.0.0',
    description='VSX2 tools web app',
    author='Vladyslav Samotoy',
    author_email='svevladislav@gmail.com',
    url='',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=requires,
    entry_points={
        'flask.commands': [
            'assets = flask_assets:assets',
        ],
        'console_scripts': [
            'vsx2_tools_web_run = vsx2_tools_web.app.server:main'
        ]
    }
)
