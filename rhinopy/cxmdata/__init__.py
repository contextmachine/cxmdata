import Rhino.Geometry as rg
import json, ast
import bz2, base64


def create_Transform(flat_arr):
    tg = rg.Transform.ZeroTransformation
    k = 0
    for i in range(4):
        for j in range(4):
            setattr(tg, "M{}{}".format(i, j), flat_arr[k])
            k += 1
    return tg


def decode(dct):
    if isinstance(dct, (list, tuple, float)) and (len(dct) == 16):
        return create_Transform(dct)
    elif isinstance(dct, (list, tuple)):

        return [decode(geom) for geom in dct]
    elif isinstance(dct, dict):
        if "archive3dm" in dct.keys():
            return rg.GeometryBase.FromJSON(json.dumps(dct))
        elif "X" in dct.keys():

            return rg.Point3d(*list(dct.values()))

        else:
            return dict([(k, decode(v)) for k, v in dct.items()])
    elif isinstance(dct, (int, float, bool, bytes, str)):
        return dct
    else:
        return dct


# a=decode(json.loads(x))

def decompress(string):
    return decode(json.loads(bz2.decompress(base64.b16decode(string.encode())).decode()))


def encode(geoms):
    if isinstance(geoms, list):
        return [encode(geom) for geom in geoms]
    elif geoms.__class__.__name__ == "Namespace":
        return dict([(k, encode(v)) for k, v in geoms.__dict__.items()])
    elif isinstance(geoms, dict):
        return dict([(k, encode(v)) for k, v in geoms.items()])
    elif hasattr(geoms, "ToJSON"):
        return ast.literal_eval(geoms.ToJSON(None))
    elif hasattr(geoms, "ToFloatArray"):
        return geoms.ToFloatArray(True)
    elif isinstance(geoms, (int, float, bool, bytes, str)):
        return geoms
    elif hasattr(geoms, "ToNurbsCurve"):
        return ast.literal_eval(geoms.ToNurbsCurve().ToJSON(None))
    else:
        raise TypeError("Can not encode this :(")


import pprint


def compress(data):
    return base64.b16encode(bz2.compress(json.dumps(encode(data)), compresslevel=9)).decode()


class CxmData(object):

    def __new__(cls, s):

        if isinstance(s, str):
            pass
        elif isinstance(s, bytes):
            s = s.decode()
        else:
            s = cls.compress(s)
        instance = object.__new__(cls)
        instance._s = s
        return instance

    def ToString(self):
        return "cxm'{}...{}'".format(self._s[:10], self._s[-10:])

    def ToJSON(self, options=None):
        if options is None:
            options = dict()
        return json.dumps(self.decompress(self._s), **options)

    def FromJSON(self, data):
        return CxmData(self.compress(json.loads(data)))

    @staticmethod
    def decompress(data):
        return decompress(data)

    @staticmethod
    def compress(data):
        return compress(data)
