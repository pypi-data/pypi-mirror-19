class Container:
    def __init__(self):
        self._bindings = []
        self._singletons = []

    def make(self, token):
        for (bound_token, singleton, factory) in self._bindings:
            if token == bound_token:
                if not singleton:
                    return factory(self)

                for (singleton_token, singleton) in self._singletons:
                    if singleton_token == token:
                        return singleton

                instance = factory(self)
                self._singletons.append((token, instance))
                return instance

        args = self._get_args(token.__init__)
        return token(**args)

    def resolve(self, function):
        args = self._get_args(function)
        return function(**args)

    def _get_args(self, function):
        if not hasattr(function, '__annotations__'):
            return {}

        args = function.__annotations__
        res = {}
        for name in args:
            res[name] = self.make(args[name])
        return res

    def bind(self, token, singleton=False):
        container = self

        class Binding:
            def to_class(self, concrete):
                container._bindings.append((
                    token,
                    singleton,
                    lambda c: container.make(concrete)
                ))

            def to_factory(self, factory):
                container._bindings.append((
                    token,
                    singleton,
                    factory
                ))

            def to_instance(self, instance):
                container._bindings.append((
                    token,
                    singleton,
                    lambda c: instance
                ))

        return Binding()
