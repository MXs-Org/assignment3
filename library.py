"""
Module for shared code that does not fit in anywhere else
"""

import requests

def make_request(injection_obj, payload, param_idx=0):
  method, link, params, cookie = injection_obj
  if method == "GET":
    res = requests.get(link, params={params[param_idx]: payload})
  else:
    # TODO: for now, this only POSTs as x-www-form-urlencoded
    # Consider adding more types in the future?
    res = requests.post(link, data={params[param_idx]: payload})
  return res