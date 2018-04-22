import sys
import requests
from bs4 import BeautifulSoup

def run(link, soup):
  print("Running {}".format(link))

  response = requests.get(link);

  print(contains_passwd(response))

def contains_passwd(response):
  """Checks if reponse constains /etc/passwd contents

  Works by checking if the response contains
  root:x:0:0:

  Args:
    response: Requests response object

  Returns:
    boolean
  """
  #TODO: need to find out if this is the best way to check /etc/passwd got displayed

  ROOT_LINE = 'root:x:0:0:'

  if response.status_code != 200:
    return False

  if ROOT_LINE in response.text:
    return True

  # TODO: in case response contains JSON use reponses.json()
  # TODO: check if necessary - maybe using .text is sufficient

  return False

# TODO for testing, remove when done
if __name__ == '__main__':

  if len(sys.argv) != 2:
    print("input link pls")

  run(sys.argv[1], None)
