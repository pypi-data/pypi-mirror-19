"""
Shaft

Views

"""
from shaft import (Shaft,
                   page_meta,
                   get_config,
                   flash_success,
                   flash_error,
                   abort,
                   request,
                   url_for,
                   redirect,
                   models,
                   utils,
                   decorators as deco
                   )

# ------------------------------------------------------------------------------


class Index(Shaft):

    @deco.menu_title("Home", order=1)
    def index(self):
        page_meta(title="Hello View!")
        return {}

    @deco.accept_get
    @deco.render_json
    def hello(self):
        return {"Hello": "World"}


