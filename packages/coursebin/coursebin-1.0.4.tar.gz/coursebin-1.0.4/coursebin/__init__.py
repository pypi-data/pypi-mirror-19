import os
import json
from helpers import _get_json, write_json, logging, _get_data
from objects import College, Semester, Course

config_path = _get_data('static/config.json')
json_opts = _get_json()
college = College(json_opts['collegeDirectory'])

