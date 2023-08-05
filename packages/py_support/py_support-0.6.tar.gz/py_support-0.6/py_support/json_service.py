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
