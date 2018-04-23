"""
Module for shared code that does not fit in anywhere else
"""

import requests

DEBUG = True
# Modify this
# TODO: maybe change this to be a command line argument?
# Note: DON'T end with a TRAILING '/'
TARGET_URL = "http://localhost:8888"
BASE_URL = "http://localhost:8888" if DEBUG else "http://target.com"


def make_request(injection_obj, payload, param_idx=0):
  method, link, params, cookie = injection_obj
  if method == "GET":
    res = requests.get(link, params={params[param_idx]: payload})
  else:
    # TODO: for now, this only POSTs as x-www-form-urlencoded
    # Consider adding more types in the future?
    res = requests.post(link, data={params[param_idx]: payload})
  return res

def make_results_obj(injection_obj, payload):
  # Makes the Python object that will eventually be turned into a JSON object
  # TODO: find out how cookie affects the results JSON
  # TODO: right now, payload is identical for every param
  method, link, params, cookie = injection_obj
  endpoint = link[len(BASE_URL):]
  obj = {
    "endpoint": endpoint,
    "params": { param: payload for param in params },
    "method": method
  }
  return obj