# BetterDotMap

Based on DotMap, this also allows dot notation in the `__getitem__` magic
method, making it easier to call on nested objects without using either loops or directly calling `__getattr__`.

You can also supply your own separator, with the init kwarg
`_separator='_'`, this applies only to the getitems.

```In [1]: import betterdotmap

In [3]: s = betterdotmap.BetterDotMap({"lol": {"heisann": [1,2,3,4,"rrr"]}})

In [4]: s
Out[4]: BetterDotMap(lol=BetterDotMap(heisann=[1, 2, 3, 4, 'rrr']))

In [5]: s.lol
Out[5]: BetterDotMap(heisann=[1, 2, 3, 4, 'rrr'])

In [6]: s['lol.heisann']
Out[6]: [1, 2, 3, 4, 'rrr']

In [7]: s.lol.heisann
Out[7]: [1, 2, 3, 4, 'rrr']```
