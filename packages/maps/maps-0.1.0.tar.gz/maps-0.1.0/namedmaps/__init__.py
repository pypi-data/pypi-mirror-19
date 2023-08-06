from namedmaps.fixedkeymap import FixedKeyMap
from namedmaps.namedfixedkeymap import NamedFixedKeyMapMeta
from namedmaps.namedfrozenmap import NamedFrozenMapMeta

def namedmap(typename, fields, mutable_values=False):
    if mutable_values:
        return NamedFixedKeyMap(typename, fields)
    return NamedMap(typename, fields)
