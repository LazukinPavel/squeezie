from flask import Flask, request, redirect
from playhouse.postgres_ext import PostgresqlDatabase

from controllers import URLCreateController, URLResultController, URLRedirectController
from models import db as db_proxy


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    init_db(app)
    init_routes(app)

    return app


def init_db(app):
    db = PostgresqlDatabase(**app.config["DB"])
    db_proxy.initialize(db)


def init_hooks(app):
    @app.before_request
    def before():
        if db_proxy.is_closed():
            db_proxy.connect()

    @app.teardown_request
    def _db_close(exc):
        if not db_proxy.is_closed():
            db_proxy.close()


def init_routes(app):
    @app.route("/result/<uuid>/<redirect_count>", methods=["GET"])
    def result(uuid, redirect_count):
        return URLResultController(request).call(uuid, redirect_count)

    @app.route("/", methods=["GET", "POST"])
    def main():
        return URLCreateController(request).call()

    @app.route("/<uuid>")
    def short_url(uuid):
        return URLRedirectController(request).call(uuid)
