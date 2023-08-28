#!/usr/bin/env python
"""Print a given Release Promotion task's input as yaml.

The input used to generate a given Release Promotion task is baked into
``task.extra.action.context.input``, but it's in json format. Let's output it
as yaml for easier manipulation.

Write the Release Promotion action to `task.json` in the current directory,
then run this script.

Requires PyYAML; written+tested with PyYAML==5.4.1, python 3.7.4

"""

import json
import yaml

with open("task.json") as fh:
    print(yaml.dump(json.load(fh)['extra']['action']['context']['input']))
