"""Routes."""


def includeme(config):
    """Include me."""
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('list', '/')
    config.add_route('detail', '/journal/{id:\d+}')
    config.add_route('create', '/journal/new-entry')
    config.add_route('update', '/journal/{id:\d+}/edit-entry')
    # TODO:
    config.add_route('delete', '/journal/{id:\d+}/delete-entry')
    config.add_route('delete_forever', '/journal/{id:\d+}/delete-forever')