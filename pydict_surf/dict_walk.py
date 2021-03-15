from abc import ABC
from collections import OrderedDict
from collections import deque
from typing import Union, Any
from jsonpath_ng import jsonpath, parse

class DictWalker(OrderedDict):
    def __init__(reference_dict:dict):
        self.reference_dict = reference_dict

    def walk(self):
       pass

    def iterate(self, mode:str = "bfs", depth:int = -1):
        iterable = SubDict_Object()
        
        iter_pointer.append()


class DictIterator(ABC):
    functional_keys = ['.', '..'] 
    def __init__(self, reference_dict:Any, dict_location:str = None):
        self.reference_dict = reference_dict
        self.dict_location = dict_location or "" 

        self.dict_pointer = self.reference_dict

    def chdict(self, key_name:str, from_root:bool = False):
        if key_name in DictIterator.functional_keys:
            if key_name == '..':
                key_name = self.dict_location[:self.dict_location.rfind('.')]
                from_root = True

        key_names = key_name.split(".")
        if from_root:
            self.dict_pointer = self.reference_dict
            self.dict_location = ""
        else:
            pass
        for key_item in key_names:
            if key_item[0] == '[':
                key_item = int(key_item[1:-1])
            self._chdict_itemwise(key_item)
        
    def _chdict_itemwise(self, key_name:Union[str, int]):
        if isinstance(key_name, int):
            if not isinstance(self.dict_pointer, list):
                raise ValueError("Int key passed while the iterable is not list or touple")
            if key_name >= len(self.dict_pointer):
                raise ValueError("Array out of bound")
            self.dict_pointer = self.dict_pointer[key_name]
            self.dict_location += f".[{key_name}]"
        elif isinstance(key_name, str) and key_name not in self.functional_keys:
            if not isinstance(self.dict_pointer, dict):
                raise ValueError("String key passed while the iterable is not dict")
            if key_name not in self.list_nested():
                raise KeyError(f"{key_name} not in nested structures")
            self.dict_pointer = self.dict_pointer[key_name]
            self.dict_location += f".{key_name}"

    def listdict(self, key_name:str = None):
        return list(self.dict_pointer.keys())
    
    def list_nested(self, key_name:str = None):
        return [
            item 
            for item in list(self.dict_pointer.keys())
            if hasattr(self.dict_pointer[item], "__iter__")
        ]

    def show(self):
        return self.dict_pointer

    def pwdict(self):
        return self.dict_location


    
    
    

