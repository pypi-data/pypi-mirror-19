import inspect


class Container:
    def __init__(self, parent=None):
        self._parent = parent
        self._bindings = []
        self._singletons = []

    def make(self, token, **kwargs):
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

        if self._parent is not None:
            return self._parent.make(token)

        args = self._get_args(token.__init__, kwargs)
        return token(**args)

    def resolve(self, function, **kwargs):
        args = self._get_args(function, kwargs)
        return function(**args)

    def _get_args(self, function, kwargs):
        if not hasattr(function, '__annotations__'):
            return kwargs

        args = function.__annotations__
        res = kwargs
        for name in args:
            res[name] = self.make(args[name])
        return res

    def fork(self):
        return Container(parent=self)

    def bind(self, token, singleton=False):
        container = self

        class Binding:
            @staticmethod
            def to_class(concrete):
                container._bindings.append((
                    token,
                    singleton,
                    lambda c: container.make(concrete)
                ))

            @staticmethod
            def to_factory(factory):
                container._bindings.append((
                    token,
                    singleton,
                    factory
                ))

            @staticmethod
            def to_instance(instance):
                container._bindings.append((
                    token,
                    singleton,
                    lambda c: instance
                ))

        return Binding()

    def curry(self, function):
        if inspect.isclass(function):
            def fun(*args, **kwargs):
                fork = self.fork()
                [fork._bind_typeof(arg) for arg in args]
                return fork.make(function, **kwargs)
            return fun

        def fun(*args, **kwargs):
            fork = self.fork()
            [fork._bind_typeof(arg) for arg in args]
            return fork.resolve(function, **kwargs)
        return fun

    def _bind_typeof(self, value):
        [self.bind(t).to_instance(value) for t in self._types(value)]

    @staticmethod
    def _types(value):
        subtypes = [t for t in type(value).__bases__ if t is not object]
        return [type(value), *subtypes]
