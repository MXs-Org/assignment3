import sys
import requests
from bs4 import BeautifulSoup

import library

def run(injection_obj_lst):
  print("[*] Testing for Open Redirect")

  payloads = get_payload_list()
  results = inject_all_injection_objs(injection_obj_lst, payloads)

  return results

def inject_all_injection_objs(injection_obj_lst, payloads):
  results = []
  for injection_obj in injection_obj_lst:
    curr_result = inject_payloads(injection_obj, payloads)
    if curr_result != None:
      results.append(curr_result)

  return results

def inject_payloads(injection_obj, payloads):
  method, link, params, cookie = injection_obj
  is_exploitable = False

  # try injection each payload into each param
  for param_idx in range(len(params)):
    for payload in payloads:
      # print("Trying {} request {} with {} as param {}".format(method, link, payload, params[param_idx]))
      response = library.make_request(injection_obj, payload, param_idx)
      is_exploitable = is_successful_redirect(response)

      if is_exploitable:
        print("Exploitable with payload {}: {}\n".format(payload, is_exploitable))
        return library.make_results_obj(injection_obj, payload)

  return None

def get_payload_list(filename='payloads/open_redirect_payloads.txt'):
  """Returns payloads in payload file as a list"""
  with open(filename) as f:
    payloads = f.read().splitlines()
    return payloads

def is_successful_redirect(response):
  """Checks if reponse constains /etc/passwd contents
  Works by checking if the response contains 'GitHub System Status'

  Args:
    response: Requests response object

  Returns:
    boolean
  """

  TITLE_LINE = 'GitHub System Status'

  if response.status_code != 200:
    return False

  if TITLE_LINE in response.text:
    return True

  # TODO: in case response contains JSON use reponses.json()
  # TODO: check if necessary - maybe using .text is sufficient
  # tested with nusmods api - probably no need to use reponses.json()

  return False

# TODO for testing, remove when done
if __name__ == '__main__':
  injection_obj_lst = [['GET','http://127.0.0.1:8888/openredirect/openredirect.php', ['redirect'], '']]
  print(run(injection_obj_lst))
