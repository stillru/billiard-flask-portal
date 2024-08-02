def route_metadata(name, category, requires_auth=False):
    def decorator(f):
        f._metadata = {
            "name": name,
            "category": category,
            "requires_auth": requires_auth,
        }
        return f

    return decorator
