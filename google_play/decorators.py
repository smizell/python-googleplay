# 
def requires_fetch(fn):
    """
    Decorator to see if item has been fetched

    If the detail page has not been fetched, this
    will call the _fetch() method, which will
    populate the fields from the details page.
    """
    def wrapper(obj, *args, **kwargs):
        if not obj._is_fetched:
            obj._fetch()
        return fn(obj, *args, **kwargs)
    return wrapper