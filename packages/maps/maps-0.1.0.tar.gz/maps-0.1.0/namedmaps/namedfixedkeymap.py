import abc
import namedmaps.utils as utils
from namedmaps.fixedkeymap import FixedKeyMap

class NamedFixedKeyMapMeta(abc.ABCMeta):
    def __new__(cls, typename, fields=[]):
        # validate names
        for name in [typename] + fields:
            utils._validate_name(name)
        utils._validate_fields(fields)

        def getattr__(self, name):
            return self._data[name]

        def setattr__(self, name, value):
            if name.startswith('_'):
                super(self.__class__, self).__setattr__(name, value)
            elif name in self._data:
                self._data[name] = value
            else:
                raise AttributeError("'{typename}' object has no attribute {name!r}")

        def repr__(self):
            kwargs = ', '.join(f'{key}={value!r}' for key, value in self.items())
            return f'{typename}({kwargs})'

        methods = {
            '__getattr__': getattr__,
            '__repr__': repr__,
            '__setattr__': setattr__}

        # handle custom __init__
        template = '\n'.join([
            'def __init__(self, {args}):',
            '    super(self.__class__, self).__init__({kwargs})'])
        args = ', '.join(fields)
        kwargs = ', '.join([f'{i}={i}' for i in fields])
        exec(template.format(args=args, kwargs=kwargs), methods)

        return super().__new__(cls, typename, (EditMap,), methods)

    def __init__(cls, name, fields=[]):
        super().__init__(cls)
