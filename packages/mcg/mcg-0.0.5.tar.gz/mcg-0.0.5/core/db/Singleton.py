class Singleton(type):

    def __init__(cls, name, bases, dic):
        type.__init__(cls, name, bases, dic)

        def __copy__(self):
            return self

        def __deepcopy__(self, memo=None):
            return self

        cls.__copy__ = __copy__
        cls.__deepcopy__ = __deepcopy__

    def __call__(cls, *args, **kwargs):
        try:
            return cls.__instance
        except AttributeError:
            cls.__instance = super(Singleton, cls).__call__(*args, **kwargs)
            return cls.__instance
