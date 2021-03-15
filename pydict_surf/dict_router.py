"""A toolkit to route inside a nested dictionary and list.
The item is specifically designed for routing inside a json dictionary. It can route inside a
key, outside it, and to a specific address. The class is also capable of updating and reading
keys. The usage of this class is almost like the os command system as it has chdict (instead of
chdir), pwdict (instead of pwd), etc
"""
from collections import deque
from typing import Union, Any


class DictRouter(object):
    functional_keys = ['.', '..']

    def __init__(self, reference_dict: Union[list, dict], dict_location: str = None):
        self.reference_dict = reference_dict
        self.dict_location = dict_location or ""

        self.dict_pointer = self.reference_dict

    def chdict(self, key_name: str, from_root: bool = False):
        if key_name in DictRouter.functional_keys:
            if key_name == '..':
                key_name = self.dict_location[:self.dict_location.rfind('.')]
                from_root = True
        if isinstance(key_name, int):
            key_name = f"[{key_name}]"
        key_names = key_name.split(".")
        if from_root:
            self._chdict_itemwise("")

        for key_item in key_names:
            if len(key_item) and key_item[0] == '[':
                key_item = int(key_item[1:-1])
            self._chdict_itemwise(key_item)

    def _chdict_itemwise(self, key_name: Union[str, int]):
        if isinstance(key_name, int):
            if not isinstance(self.dict_pointer, list):
                raise ValueError("Int key passed while the iterable is not list or touple")
            if key_name >= len(self.dict_pointer):
                raise ValueError("Array out of bound")
            self.dict_pointer = self.dict_pointer[key_name]
            self.dict_location += f".[{key_name}]"
        elif isinstance(key_name, str):
            if key_name == "":
                self.dict_pointer = self.reference_dict
                self.dict_location = ""
                return
            if not isinstance(self.dict_pointer, dict):
                raise ValueError("String key passed while the iterable is not dict")
            if key_name not in self.list_nested():
                raise KeyError(f"{key_name} not in nested structures")
            self.dict_pointer = self.dict_pointer[key_name]
            self.dict_location += f".{key_name}"

    def listdict(self, key_name: str = None):
        if isinstance(self.dict_pointer, dict):
            return list(self.dict_pointer.keys())
        elif isinstance(self.dict_pointer, list):
            return list(range(len(self.dict_pointer)))
        else:
            raise ValueError("Object type is not supported; only list and dict is acceptable")

    def list_nested(self, key_name: str = None):
        return [
            item
            for item in self.listdict()
            if isinstance(self.dict_pointer[item], (list, dict))
        ]

    def list_flats(self, key_name: str = None):
        return [
            item
            for item in self.listdict()
            if not isinstance(self.dict_pointer[item], (list, dict))
        ]

    def show(self):
        return self.dict_pointer

    def pwdict(self):
        return self.dict_location

    def update(self, key, value, force=True):
        if '.' in key:
            if key in self.listdict() or force:
                self.dict_pointer[key] = value
            else:
                raise KeyError(f"Key: {key} Does not exist")
        else:
            relocation_addr = key[:key.rfind(".")]
            key = key.split(".")[-1]
            backup_addr = self.dict_location
            self.chdict(relocation_addr)
            self.update(key, value, force)
            self.chdict(backup_addr)

    def get(self, key, default=None):
        if '.' in key:
            if key in self.listdict():
                return self.dict_pointer[key]
            else:
                return default
        else:
            relocation_addr = key[:key.rfind(".")]
            key = key.split(".")[-1]
            backup_addr = self.dict_location
            self.chdict(relocation_addr)
            value = self.get(key, default)
            self.chdict(backup_addr)
            return value

    def walk(self, key: str = None, traversal_method='bfs', max_depth: int = -1):
        key = key or ""
        backup_addr = self.dict_location
        self.chdict(key)
        traversal_items = self.traversal(traversal_method, max_depth=max_depth)
        self.chdict(backup_addr)
        for items in traversal_items:
            yield items

    def traversal(self, traversal_method='bfs', max_depth: int = -1):
        traversal_items = []
        dq = deque()
        dq.append((
            self.pwdict(),
            self.list_nested(),
            self.list_flats(),
            0
        ))

        while len(dq):
            item = dq.pop()
            if max_depth != -1 and item[-1] > max_depth:
                continue
            traversal_items.append(item[:-1])

            self.chdict(item[0])
            for sub_item in self.list_nested():
                self.chdict(sub_item)
                if traversal_method == "bfs":
                    dq.append((
                        self.pwdict(),
                        self.list_nested(),
                        self.list_flats(),
                        item[-1] + 1
                    ))
                elif traversal_method == "dfs":
                    dq.appendleft((
                        self.pwdict(),
                        self.list_nested(),
                        self.list_flats(),
                        item[-1] + 1
                    ))
                self.chdict("..")

        return traversal_items
