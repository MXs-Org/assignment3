import sys
import requests
import library
from bs4 import BeautifulSoup

def run(injection_obj_lst):
  print("[*] Testing for Directory Traversal")

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

  # for each param, try all payloads
  for param_idx in range(len(params)):
    for payload in payloads:
      # print("Trying {} request {} with {} as param {}".format(method, link, payload, params[param_idx]))
      response = library.make_request(injection_obj, payload, param_idx)
      is_exploitable = contains_passwd(response)

      if is_exploitable:
        print("Exploitable with payload {}: {}\n".format(payload, is_exploitable))        
        return library.make_results_obj(injection_obj, payload)

  return None

def get_payload_list(filename='payloads/directory_traversal_payloads.txt'):
  """Returns payloads in payload file as a list"""
  with open(filename) as f:
    payloads = f.read().splitlines()
    return payloads

def contains_passwd(response):
  """Checks if reponse constains /etc/passwd contents
  Works by checking if the response contains 'root:x:0:0:'

  Args:
    response: Requests response object

  Returns:
    boolean
  """
  # TODO: need to find out if this is the best way to check /etc/passwd got displayed\
  #       maybe just change to ':x:0:0' because the username of root user may not always be root
  #       but the uid and gid is guaranteed to be 0

  ROOT_LINE = 'root:x:0:0:'

  if response.status_code != 200:
    return False

  if ROOT_LINE in response.text:
    return True

  # TODO: in case response contains JSON use reponses.json()
  # TODO: check if necessary - maybe using .text is sufficient
  # tested with nusmods api - probably no need to use reponses.json()

  return False

# TODO for testing, remove when done
if __name__ == '__main__':
  injection_obj = [['GET','http://127.0.0.1:8888/directorytraversal/directorytraversal.php', ['ascii'], ''], ['GET','http://127.0.0.1:8888/directorytraversal/directorytraversal.php', ['ascii'], '']]
  import pprint
  pprint.pprint(run(injection_obj))
