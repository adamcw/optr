import copy

class Options(object):
    
    def __init__(self, groups, default=None, argmap=None):
        '''Underscores have been placed in front of variable 
        names so that __getattr__ can be used to access the 
        underlying options without naming collisions.'''

        # Will be the name of the default group
        self.__default_name = "default"

        # The key to use, indicating to use the default value
        self.__default_val = "__default__"

        # The name of the mixin attribute
        self.__mixin_attr = "mixin"

        self.__argmap = argmap or {}
        self.__opts = {}
    
        default = copy.deepcopy(default) if default is not None else {}
        self.__groups = {self.__default_name: default}
        self.__groups.update(groups)
        
        self._add(default)

    def _add(self, ndict):
        self.__update_dict(self.__opts, ndict) 
        return self
    
    def _resolve(self, groups):
        groups = [groups] if isinstance(groups, str) else groups
        self.__resolve_groups(groups, self.__opts)
        return self

    def _reset(self):
        self.__opts = {}
        self._add(self.__groups[self.__default_name])
        return self

    def __update_dict(self, odict, ndict):
        if not isinstance(ndict, dict):
            return odict

        # Resolve mixins before anything else
        if self.__mixin_attr in ndict:  
            mixin = self.__resolve_groups(ndict[self.__mixin_attr])
            odict.update(mixin)

        # Sort so that all advanced functions execute first
        # as they may be overwritten by non-advanced functions
        opts = sorted(ndict.items(), key=lambda t: t[0] not in self.__argmap)

        for attr, val in opts:
            if attr == self.__mixin_attr:
                continue

            # Resolve default keyword first
            if val == self.__default_val:
                val = self.__groups[self.__default_name][attr]

            # If advanced, execute the function
            if attr in self.__argmap:
                self.__update_dict(odict, self.__argmap[attr](val))
                continue

            # If the result is a dict, resolve
            if isinstance(val, dict) and attr in odict:
                val = self.__update_dict(odict[attr], val)
        
            odict.update({attr: val})

        return odict
 
    def __resolve_groups(self, groups, opts=None):
        opts = opts if opts is not None else {}
        for group in groups:
            self.__update_dict(opts, self.__groups[group])
        return opts

    # Required in order to be able to kwargs
    def keys(self): return self.__opts.keys()

    def __str__(self): return str(self.__opts)
    def __getattr__(self, i): return self.__opts[i]
    def __getitem__(self, i): return self.__opts[i]
    def __cmp__(self, dict): return cmp(self.__opts, dict)

