def build_method_handlers(method, handler_names, loader):
    def func(**kwargs):
        for handler_name in handler_names:
            handler = loader.get_method_handler(handler_name)
            handler(kwargs)

        return method(**kwargs)

    return func
