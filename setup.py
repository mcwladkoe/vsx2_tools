from setuptools import setup, find_packages

requires = [
    "cssmin==0.2.0",
    "flask==2.0.1",
    "Flask-Assets==2.0",
    "flask_babel==2.0.0",
    "jsmin==2.2.2",
    "Pillow==8.3.1",
    "pyclamd==0.4.0",
    "waitress==2.0.0",
    "Flask-WTF==0.15.1",
    "vsx2_change_layout @ git+https://github.com/mcwladkoe/vsx2_change_layout",
    "vsx2_rotate @ git+https://github.com/mcwladkoe/vsx2_rotate",
]

setup(
    name="vsx2_tools_web",
    description="VSX2 tools web app",
    author="Vladyslav Samotoy",
    author_email="me@vldsx.com",
    url="",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=requires,
    entry_points={
        "flask.commands": [
            "assets = flask_assets:assets",
        ],
        "console_scripts": ["vsx2_tools_web_run = vsx2_tools_web.app.server:main"],
    },
)
