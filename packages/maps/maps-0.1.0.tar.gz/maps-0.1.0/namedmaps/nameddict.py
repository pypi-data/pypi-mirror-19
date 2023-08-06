import collections.abc
import namedmaps.utils as utils

class NamedDict(collections.abc.MutableMapping):
    def __init__(self, *args, **kwargs):
        data = dict(*args, **kwargs)
        for key in data:
            utils._validate_name(key)
        utils._validate_fields(data.keys())
        self._data = data

    def __delitem__(self, name):
        del self._data[name]

    def __getattr__(self, name):
        return self._data[name]

    def __getitem__(self, name):
        return self._data[name]

    def __iter__(self, name):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__getattr__(name, value)
        else:
            self._data[name] = value

    def __setitem__(self, name, value):
        if name.startswith('_'):
            raise ValueError(
                f'Field names cannot start with an underscore: {name!r}')
        self._data[name] = value

    def __repr__(self):
        kwargs = ', '.join(f'{key}={value!r}' for key, value in sorted(self.items()))
        return f'{self.__class__.__name__}({kwargs})'
