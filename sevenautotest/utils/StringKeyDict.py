# -*- coding:utf-8 -*-
"""

"""

__version__ = "1.0"
__author__ = "si wen wei"

# from collections import MutableMapping #DeprecationWarning: Using or importing the ABCs from 'collections' instead of from 'collections.abc' is deprecated since Python 3.3, and in 3.9 it will stop working
from collections.abc import MutableMapping


class StringKeyDict(MutableMapping):
    def __init__(self, initial=None, remove_chars=(), to_lower_case=True, remove_all_whitespace=True):

        self._data = {}
        self._keys = {}
        self.remove_chars = remove_chars
        self.to_lower_case = to_lower_case
        self.remove_all_whitespace = remove_all_whitespace
        if initial:
            self._add_initial(initial)

    def _normalize_string(self, string):

        empty = ""
        if self.remove_all_whitespace:
            string = empty.join(string.split())
        if self.to_lower_case:
            string = string.lower()
            self.remove_chars = [c.lower() for c in self.remove_chars]
        if self.remove_chars:
            for remove_char in self.remove_chars:
                if remove_char in string:
                    string = string.replace(remove_char, empty)
        return string

    def _add_initial(self, initial):

        items = initial.items() if hasattr(initial, 'items') else initial
        for key, value in items:
            self[key] = value

    def __getitem__(self, key):

        return self._data[self._normalize_string(key)]

    def __setitem__(self, key, value):

        lower_key = self._normalize_string(key)
        self._data[lower_key] = value
        self._keys.setdefault(lower_key, key)

    def __delitem__(self, key):

        lower_key = self._normalize_string(key)
        del self._data[lower_key]
        del self._keys[lower_key]

    def __iter__(self):

        return (self._keys[lower_key] for lower_key in sorted(self._keys))

    def __len__(self):

        return len(self._data)

    def __str__(self):

        return '{%s}' % ', '.join('%r: %r' % (key, self[key]) for key in self)

    def __eq__(self, other):

        if isinstance(other, StringKeyDict):
            return self._data == other._data
        else:
            return False

    def __ne__(self, other):

        return not self == other

    def __contains__(self, key):

        return self._normalize_string(key) in self._data

    def clear(self):

        self._data.clear()
        self._keys.clear()


if __name__ == "__main__":

    alias = StringKeyDict()
    alias["KEY"] = 1
    d = alias
    print(alias == d)
    print(alias["key"])
