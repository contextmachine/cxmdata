# Contextmachine Data Format
## Prequest
Основным пакетом является `cxmdata`. Все остальные пакеты в каталоге существуют для использования формата внутри сторонних пакетов.

## Description
СxmData allows you to combine data from different sources and create custom data decoders/encoders. 
You just pass the dependencies and decode what you want into simple python dictionaries or json.\

### Example:
 In this case, we make an array with `RhinoCommon` objects in RhinoPython. We can decode it with a `rhino3dm` library.
    However, we need a more complex data structure and custom attributes.
```python
from cxmdata import CxmData


with open("examples/basic/example.cxm","r") as d:
    cxm=CxmData(d.read())
```
Result:
```doctest
>>> cxm.decompress()
({'values': [<rhino3dm._rhino3dm.PolyCurve at 0x14cd440f0>, 'P-L-1-5-1'],
 'keys': ['k1', 'k2']},
{'values': [<rhino3dm._rhino3dm.PolyCurve at 0x14cd441f0>, 'P-L-1-5-2'],
 'keys': ['k1', 'k2']},

...
 ```
CxmData представляет собой строку, приведенную к ASCII с помощью [Base64](https://en.wikipedia.org/wiki/Base64). 
Поэтому она может быть безопасно передана в любое api а также упростит вам работу с вашим сервисом из под с чужого api

### Patterns
Формат создан для передечи данных по сети с использованием http, ws, а также с помощью сокетов. Поэтому нет особой необходимости в файловом представлении.
Однако на тот случай если хранение данных в файловой системе принципиально файл может быть сохранен в виде bz, gzip архива с расширениями:
```
*.cxm *.cxz 
```
For example, with using Pycharm:
![img_1.png](img_1.png)