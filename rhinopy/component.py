
import Grasshopper as gh
import GH_IO

class Getter(object):
    def __call__(self):
        global pyObj, key
        return pyObj[key]

