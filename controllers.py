import validators
from urllib.parse import urljoin

from flask import abort, redirect, url_for, render_template, current_app

from models import Url


class URLController:
    def __init__(self, request):

        self.request = request
        self.method = request.method

    def call(self, *args, **kwargs):
        try:
            return self._call(*args, **kwargs)
        except ValidationError as e:
            current_app.logger.error(str(e))
            return render_template("error.html", error=str(e))
        except Exception as e:
            current_app.logger.error(str(e))
            return render_template("error.html", error="Service Error")

    def _call(self, *args, **kwargs):
        raise NotImplementedError("%s._call" % self.__class__.__name__)


class URLCreateController(URLController):
    def __init__(self, request):
        super().__init__(request)
        current_app.logger.info(f"Request form data: {dict(request.form)}")

    def _call(self, *args, **kwargs):
        if self.method == "POST":
            form_data = self.request.form
            origin_url = form_data["origin_url"]

            if not validators.url(origin_url):
                raise ValidationError(f"Not a valid url provided: {origin_url}")

            url, created = Url.get_or_create(origin=origin_url)

            if not created:
                url.redirect_count += 1
                url.save(only=[Url.redirect_count])

            return redirect(
                url_for("result", uuid=url.uuid, redirect_count=url.redirect_count)
            )

        return render_template("main.html")


class URLResultController(URLController):
    def _call(self, uuid, redirect_count):
        short_url = urljoin(current_app.config["BASE_URL"], str(uuid))

        return render_template(
            "result.html", short_url=short_url, redirect_count=redirect_count
        )


class URLRedirectController(URLController):
    def _call(self, uuid):
        url = Url.get_or_none(Url.uuid == uuid)
        if url is not None:
            return redirect(url.origin)

        abort(404)


class ValidationError(Exception):
    pass
