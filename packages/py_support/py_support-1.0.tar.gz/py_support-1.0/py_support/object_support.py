# -*- coding: utf-8 -*-
#!/usr/bin/python

import sys
import os
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
from py_support.logger_service import Logger
from py_support.json_service import JsonWorker

logger = Logger()
json_worker = JsonWorker()


def get_keys(obj_class, mapping):
    """ get keys from mapping by model (obj_class) """
    return mapping[obj_class]


def get_object(json_obj, model, key_index, prefix, mapping):
    """ get object from json, where key_index is ind in mapping """
    # logger.info("JSON: %s" % json_worker.human_view(json_obj))
    keys = get_keys(model, mapping)
    try:
        # logger.log(keys[key_index])
        if prefix:
            extracted = json_obj[prefix][keys[key_index]]
        else:
            # update have None prefix as root of tree
            extracted = json_obj[keys[key_index]]
        # for basic models mapping
        if type(extracted) is dict:
            obj = model(**extracted)
        # for list models mapping
        else:
            obj = []
            for item in extracted:
                obj.append(model(**item))
        return obj
    except KeyError:
        return None


class DefaultBuilder:
    """ abstract builder for all entities """
    logger = logger

    def __init__(self):
        pass

    def _get_simple_field(self, json_obj, key_name):
        return json_worker.keylist_exist(json_obj,
            (self.prefix, key_name))[0]

