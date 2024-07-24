"""docstring"""
from flask import Flask
from board import pages

def create_app(test_config=None):
    """docstring"""
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(pages.bp)


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    return app
