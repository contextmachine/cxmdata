import ast
import base64
import bz2
import json

IS_INSIDE_RHINOCODE = False
try:
    import Rhino.Geometry as rg

    IS_INSIDE_RHINOCODE = True

except:
    import rhino3dm as rg

    IS_INSIDE_RHINOCODE = False

__all__ = ["CxmData"]


def create_Transform(flat_arr):
    tg = rg.Transform.ZeroTransformation()
    k = 0
    for i in range(4):
        for j in range(4):
            setattr(tg, "M{}{}".format(i, j), flat_arr[k])
            k += 1
    return tg


class CxmData(bytes):
    """
    Example of usage.
    In this case we make data array with RhinoCommon objects in RhinoPython. We can decode it with rhino3dm library.
    However, we need a more complex data structure and custom attributes.
    СxmData allows you to combine data from different sources and create custom data decoders/encoders.
    You just pass the dependencies and decode what you want into simple python dictionaries or json.
    >>> import json
    >>> import rhino3dm as rg
    >>> from cxmdata import CxmData
    >>> with open("examples/basic/example.cxm","r") as d:
    ...     cxm=CxmData(d.read())
    >>> cxm.decompress()
    [{'values': [<rhino3dm._rhino3dm.PolyCurve at 0x14cd440f0>, 'P-L-1-5-1'],
     'keys': ['k1', 'k2']},
    {'values': [<rhino3dm._rhino3dm.PolyCurve at 0x14cd441f0>, 'P-L-1-5-2'],
     'keys': ['k1', 'k2']},

    ...

    {'values': [<rhino3dm._rhino3dm.PolyCurve at 0x14cd453f0>, 'P-L-1-14-2'],
     'keys': ['k1', 'k2']},
    {'values': [<rhino3dm._rhino3dm.PolyCurve at 0x14cd454f0>, 'P-L-1-15-1'],
     'keys': ['k1', 'k2']}]

    """

    def __new__(cls, s, *args, **kwargs):
        print(f"IS_INSIDE_RHINOCODE: {IS_INSIDE_RHINOCODE}")
        if isinstance(s, str):
            return super().__new__(cls, s.encode(), **kwargs)
        elif isinstance(s, bytes):
            return super().__new__(cls, s, **kwargs)
        else:
            return cls.compress(s)

    @classmethod
    def _decode_to_dict(cls, dct):
        if isinstance(dct, list):
            return [cls._decode_to_dict(geom) for geom in dct]

        elif isinstance(dct, dict):
            if "archive3dm" in dct.keys():
                dct["archive3dm"] = 70
                if IS_INSIDE_RHINOCODE:
                    return rg.GeometryBase.FromJSON(json.dumps(dct))
                else:
                    return rg.GeometryBase.Decode(dct)
            elif "X" in dct.keys():
                return rg.Point3d(*list(dct.values()))
            else:
                return dict([(k, cls._decode_to_dict(v)) for k, v in dct.items()])
        elif isinstance(dct, (int, float, bool, bytes, str)):
            return dct
        else:
            return dct

    def decompress(self):
        return self._decode_to_dict(json.loads(bz2.decompress(base64.b16decode(self)).decode()))

    @classmethod
    def _encode_to_cxm(cls, geoms):
        if IS_INSIDE_RHINOCODE:

            if hasattr(geoms, "ToJSON"):
                return ast.literal_eval(geoms.ToJSON(None))

            elif hasattr(geoms, "ToFloatArray"):
                return geoms.ToFloatArray(True)
            elif isinstance(geoms, (int, float, bool, bytes, str)):
                return geoms
            elif hasattr(geoms, "ToNurbsCurve"):

                return ast.literal_eval(geoms.ToNurbsCurve().ToJSON(None))
            elif isinstance(geoms, rg.Point3d):
                return {"X": geoms.X, "Y": geoms.Y, "Z": geoms.Z}
            elif isinstance(geoms, list):
                return [cls._encode_to_cxm(geom) for geom in geoms]



            elif isinstance(geoms, dict):
                return dict([(k, cls._encode_to_cxm(v)) for k, v in geoms.items()])


            else:
                raise TypeError(f"Can not encode this :( {geoms}")
        else:
            if isinstance(geoms, list):
                return [cls._encode_to_cxm(geom) for geom in list(geoms)]
            elif isinstance(geoms, dict):
                return dict([(k, cls._encode_to_cxm(v)) for k, v in geoms.items()])
            elif hasattr(geoms, "Encode"):
                return geoms.Encode()
            elif hasattr(geoms, "ToJSON"):
                return ast.literal_eval(geoms.ToJSON(None))
            elif isinstance(geoms, rg.Point3d):
                return {"X": geoms.X, "Y": geoms.Y, "Z": geoms.Z}
            elif hasattr(geoms, "ToFloatArray"):
                return geoms.ToFloatArray(True)
            elif isinstance(geoms, (int, float, bool, bytes, str)):
                return geoms
            elif hasattr(geoms, "ToNurbsCurve") and not hasattr(geoms, "ToJSON"):

                return cls._encode_to_cxm(geoms.ToNurbsCurve())
            else:
                raise TypeError(f"Can not encode this :( {geoms}")

    @classmethod
    def compress(cls, data):
        return cls(
            base64.b16encode(bz2.compress(json.dumps(cls._encode_to_cxm(data)).encode(), compresslevel=9)).decode())
