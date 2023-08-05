# -*- coding: utf-8 -*-
#!/usr/bin/python
import json
from colored import stylize, fg


class JsonWorker:

    def __init__(self):
        pass

    def human_view(self, incoming):
        return stylize(json.dumps(incoming, indent=2, sort_keys=True),
             fg("indian_red_1a"))

    def get_json_from_request(self, request):
        """ decoded utf8 and loaded with json """
        decoded_req = request.body.decode('utf8')
        json_request = json.loads(decoded_req)
        return json_request

    def keylist_exist(self, json_object, key_list):
        """ return list with value for keys and traceback or [None] on error """
        result_list = []
        for key in key_list:
            if key:
                try:
                    json_object = json_object[key]
                except KeyError:
                    return [None]
                result_list.append(json_object)

        return result_list[::-1]


