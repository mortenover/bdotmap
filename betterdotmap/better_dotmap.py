import json
import dotmap
from pprint import pprint, pformat
from collections import OrderedDict
from inspect import ismethod


class BetterDotMap(dotmap.DotMap):

    def __init__(self, *args, **kwargs):
        self._map = OrderedDict()
        self._dynamic = True
        self._separator = '.'
        if kwargs:
            if '_dynamic' in kwargs:
                self._dynamic = kwargs['_dynamic']
            if '_separator' in kwargs:
                self._separator = kwargs['_separator']
        if args:
            d = args[0]
            # for recursive assignment handling
            trackedIDs = {id(d): self}
            if isinstance(d, dict):
                for k,v in self.__call_items(d):
                    if isinstance(v, dict):
                        if id(v) in trackedIDs:
                            v = trackedIDs[id(v)]
                        else:
                            v = BetterDotMap(v, _dynamic=self._dynamic, _separator=self._separator)
                            trackedIDs[id(v)] = v
                    if type(v) is list:
                        l = []
                        for i in v:
                            n = i
                            if isinstance(i, dict):
                                n = BetterDotMap(i, _dynamic=self._dynamic, _separator=self._separator)
                            l.append(n)
                        v = l
                    self._map[k] = v
        if kwargs:
            for k,v in self.__call_items(kwargs):
                if k not in ('_dynamic', '_separator'):
                    self._map[k] = v

    def __call_items(self, obj):
        if hasattr(obj, 'iteritems') and ismethod(getattr(obj, 'iteritems')):
            return obj.iteritems()
        else:
            return obj.items()

    def __str__(self):
        items = []
        for k, v in self.__call_items(self._map):
            # recursive assignment case
            if id(v) == id(self):
                items.append('{0}=BetterDotMap(...)'.format(k))
            else:
                items.append('{0}={1}'.format(k, repr(v)))
        joined = ', '.join(items)
        out = '{0}({1})'.format(self.__class__.__name__, joined)
        # return json.dumps(self._map, indent=4, )
        return out

    def __getitem__(self, k):
        # self[item]

        ks = k.split(self._separator)
        if self._separator in k and ks[0] in self._map and self._dynamic:
            return self._map[ks[0]][self._separator.join(ks[1:])]

        elif k not in self._map and self._dynamic and k != '_ipython_canary_method_should_not_exist_':
            # automatically extend to new DotMap
            # self[k] = BetterDotMap(_dynamic=self._dynamic, _separator=self._separator)
            raise KeyError('No such key here')
        return self._map[k]

    def __getattr__(self, k):
        # like a self.attr

        if k == '_separator':
            return super(BetterDotMap, self).__dict__['_separator']

        if k in {'_map', '_dynamic', '_ipython_canary_method_should_not_exist_', '_separator'}:
            super(BetterDotMap, self).__getattr__(k)
        else:
            return self[k]

    def __setattr__(self, k, v):

        if k in {'_map', '_dynamic', '_ipython_canary_method_should_not_exist_', '_separator'}:
            super(OrderedDict, self).__setattr__(k, v)

        else:
            self[k] = v

    def __setitem__(self, k, v):

        self._map[k] = v

    def __eq__(self, other):
        if other is None and self._map == {}:
            return True

        other = dotmap.DotMap.parseOther(other)
        if not isinstance(other, dict):
            return False

        return self._map.__eq__(other)

