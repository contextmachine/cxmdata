import pprint, copy




class Namespace:

    def __init__(self, **kwargs):
        self.keys,self.values= list(kwargs.keys()),list(kwargs.values())

    def items(self):
        return zip(self.keys, self.values)

    def __getitem__(self, k):
        return self.values[self.keys.index(k)]

    def gh_getitem(self, k):
        return self.values[self.keys.index(k)]

    def __repr__(self):
        return self.__class__.__name__ + "(" + pprint.pformat(dict(zip(self.keys, self.values))) + ")"

    def __str__(self):
        return self.__class__.__name__ + "(" + pprint.pformat(dict(zip(self.keys, self.values))) + ")"

    def ToString(self):
        return self.__str__()

class NamespaceComponent(object):
    def __new__(cls, ghenv, glbs):
        item_ = object.__new__(cls)

        item_.keys = [inp.Name for inp in ghenv.Params.Input]
        item_.values = []
        for k in item_.keys:
            item_.values.append(glbs.get(k))
        return Namespace(**dict(zip(item_.keys, item_.values)))
