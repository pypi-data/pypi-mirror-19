#!/usr/bin/env python

class autoprop(object):

    __version__ = '0.0.3'
    property = type('property', (property,), {})

    def __new__(self, cls):
        # These imports have to be inside autoprop(), otherwise the sys.modules 
        # hack below somehow makes them unavailable when the decorator is 
        # applied.
        import inspect, re
        from collections import defaultdict

        if not hasattr(cls, '__class__'):
            raise TypeError('@autoprop can only be used with new-style classes')

        accessors = defaultdict(dict)
        expected_num_args = {'get': 0, 'set': 1, 'del': 0}

        # The accessors we're searching for are considered methods in python2 
        # and functions in python3.  They behave the same either way.
        ismethod = lambda x: inspect.ismethod(x) or inspect.isfunction(x)

        for method_name, method in inspect.getmembers(cls, ismethod):
            accessor_match = re.match('(get|set|del)_(.+)', method_name)
            if not accessor_match:
                continue

            # Suppress a warning by using getfullargspec() if it's available 
            # and getargspec() if it's not.
            try: from inspect import getfullargspec as getargspec
            except ImportError: from inspect import getargspec

            prefix, name = accessor_match.groups()
            arg_spec = getargspec(method)
            num_args = len(arg_spec.args) - len(arg_spec.defaults or ())
            num_args_minus_self = num_args - 1

            if num_args_minus_self != expected_num_args[prefix]:
                continue

            accessors[name][prefix] = method

        for name in accessors:
            try:
                attr = getattr(cls, name)
                ok_to_overwrite = isinstance(attr, self.property)
            except AttributeError:
                ok_to_overwrite = True

            if ok_to_overwrite:
                setattr(cls, name, self.property(
                    accessors[name].get('get'),
                    accessors[name].get('set'),
                    accessors[name].get('del'),
                ))

        return cls


# Abuse the import system so that the module itself can be used as a decorator.  
# This is a simple module intended only to cut-down on boilerplate, so I think 
# the trade-off between magicalness and ease-of-use is justified in this case.
import sys
sys.modules[__name__] = autoprop
