# -*- coding: utf-8 -*-

# Copyright (c) 2021 by DeepLn
# Distributed under the MIT software license, see the accompanying
# Subscribe the book depth infomation

import ast, copy, json, random, string, time
from decimal import Decimal

def current_timestamp():
    return int(round(time.time() * 1_000))

def random_id(scope=10):
    return random.randint(10 ** scope, 10 ** (scope+1) - 1)

def random_order_id():
    def id_generate(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
    return "%s:%s-%s" % (id_generate(), id_generate(), id_generate())

def check_filled(param, value):
    if not value:
        raise Exception("param<%s> should be filled" % param)

class Dict2Class(object):
    replace_fields = [("null", "None"), ("true", "True"), ("false", "False")]
    def __init__(self, jdict: 'dict', recursion=True):
        def convert(v, recursion):
            if recursion:
                return Dict2Class.from_val(v)
            return v
        for k, v in jdict.items():
            setattr(self, k, convert(v, recursion))

    def hasattr(self, attr: 'str'):
        return hasattr(self, attr)

    def hasattrs(self, attrs: 'list'):
        for attr in attrs:
            if not hasattr(self, attr):
                return False
        return True

    def setattr(self, attr: 'str', val):
        setattr(self, attr, val)
        return self

    def __it_list(self, val: 'list', _4_json):
        _r = list()
        for ele in val:
            if isinstance(ele, Dict2Class):
                _r.append(ele.asdict())
            elif isinstance(ele, dict):
                _r.append(Dict2Class(ele).asdict())
            elif isinstance(ele, list):
                _r.append(self.__it_list(ele, _4_json))
            elif isinstance(ele, tuple):
                _r.append(tuple(self.__it_list(list(ele), _4_json)))
            elif _4_json and isinstance(ele, Decimal):
                _r.append(str(ele))
            else:
                _r.append(ele)
        return _r

    def asdict(self, _4_json=False):
        _d = copy.deepcopy(vars(self))
        for k, v in _d.items():
            if isinstance(v, Dict2Class):
                _d.update({k: v.asdict()})
            elif isinstance(v, dict):
                _d.update({k: Dict2Class(v).asdict()})
            elif isinstance(v, list):
                _d.update({k: self.__it_list(v, _4_json)})
            elif isinstance(v, tuple):
                _d.update({k: tuple(self.__it_list(list(v), _4_json))})
            elif _4_json and isinstance(v, Decimal):
                _d.update({k: str(v)})
        return _d

    def asstr(self):
        return json.dumps(self.asdict(_4_json=True))

    @staticmethod
    def from_val(val, recursion=True):
        if isinstance(val, dict):
            return Dict2Class(val, recursion)
        elif isinstance(val, list):
            return [Dict2Class.from_val(ele, recursion) for ele in val]
        elif isinstance(val, tuple):
            return tuple([Dict2Class.from_val(ele, recursion) for ele in val])
        return val

    @staticmethod
    def to_val(obj):
        if isinstance(obj, list):
            return [(ele.asdict() if isinstance(ele, Dict2Class) else Dict2Class.to_val(ele)) for ele in obj]
        elif isinstance(obj, Dict2Class):
            return obj.asdict()
        return obj

    @staticmethod
    def from_str(val, recursion=True):
        if isinstance(val, str):
            for (k, v) in Dict2Class.replace_fields:
                if k in val:
                    val = val.replace(k, v)
            return Dict2Class.from_val(ast.literal_eval(val), recursion)
        return Dict2Class.from_val(val, recursion)
