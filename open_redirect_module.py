import sys
import requests
from bs4 import BeautifulSoup

def run(link, soup):
  print("Running {}\n".format(link))

  payloads = get_payload_list()

  # TODO add checks
  # if link is a get request
  send_get_request(link, None, payloads)

  # else if link is post request
  # send_post_request(link, None, payloads)

def get_payload_list(filename='open_redirect_payloads.txt'):
  """Returns payloads in payload file as a list"""
  with open(filename) as f:
    payloads = f.read().splitlines()
    return payloads

def send_get_request(link, soup, payloads):
  """Try payloads in a get request"""
  for payload in payloads:
    # TODO for the time being, assumes that:
    # 1. there is only one param
    # 2. link given to it includes the param name
    # e.g. http://target.com/openredirect/openredirect.php?redirect=

    full_link = link + payload
    print("Trying get request {}".format(full_link))
    response = requests.get(full_link)
    is_exploitable = is_successful_redirect(response)
    print("Exploitable with payload {}: {}\n".format(payload, is_exploitable))

    # stop after finding the first payload that can be used to exploit the endpt
    # because if can be exploited with ../../ then for sure can be exploited with ../../../
    if is_exploitable:
        break

def send_post_request(link, soup, payloads):
  """Try payloads in a post request"""
  for payload in payloads:
    # TODO change post request
    # 1. params and link?
    # 2. headers?
    # 3. need to send data as JSON?

    print("Trying post request {}".format(link))
    response = requests.post(link, data = {'key':payload})
    is_exploitable = is_successful_redirect(response)
    print("Exploitable with payload {}: {}\n".format(payload, is_exploitable))

    # stop after finding the first payload that can be used to exploit the endpt
    # because if can be exploited with ../../ then for sure can be exploited with ../../../
    if is_exploitable:
        break

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

  if len(sys.argv) != 2:
    print("input link pls")
  else:
    run(sys.argv[1], None)
