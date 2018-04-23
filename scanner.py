# Driver for the scanning process
# Import individual attacking module here

import requests
from bs4 import BeautifulSoup

import sql_injection_module

def check_injection_points(soup):
  """Checks if the target page has any injectable elements

  Should this be a very preliminary check? Or is this check even necessary?
  Implement later. Do the invidivual module checker first!

  Looks out for the following: 
    1. <form> and <input> tags
    2. <a href> elements with query parameters
    3. URL with query parameters? (or should the module check it)

  Args:
    soup: BeautifulSoup object
  
  Returns:
    List of (link, soup, [injectable elements?])
  """
  return True

def make_json_results(results_lst):
  # Stub method
  # Creates the final results JSON needed for submission
  for result in results_lst:
    pass

def scan(link, soup):
  if check_injection_points(soup):
    print("[*] Testing endpoint: {}".format(link))
    sql_results = sql_injection_module.run(link, soup)
  return make_json_results([sql_results])

def test_vuln_modules(soup):
  sql_injection_module.run(soup)

def scan_stub(link, soup):
  # Temporary implementation of scan
  print(link)