from .registry import register_search_index as register  # noqa isort:skip
from .index import SearchIndex  # noqa

default_app_config = "lego.apps.search.apps.SearchConfig"
