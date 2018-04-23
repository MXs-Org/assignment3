# Driver for the scanning process
# Import individual attacking module here

import urlparse

import requests
from bs4 import BeautifulSoup

import sql_injection_module
from crawler import create_full_link

# Global variables. Configure COOKIE if necessary.
# Global list of injection objects is used to prevent duplicate attacks on same endpoint
COOKIE = ""
GET_INJECTION_OBJECTS = []
POST_INJECTION_OBJECTS = []

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

def extract_post_fields(link, soup):
  # Finds all possible SQL injection points present on the page
  # Returns { post_url: [list of fields] }
  output = []
  for form in soup.find_all('form'):
    if form.get('method') == "POST":
      # Extract the URL that the <form> is POSTing to
      post_url = link if not form.get('action') else link+form.get('action')
      # Extract the injectable HTML elements present in the <form>
      for child in form.find_all(recursive=False):
        params = []
        if child['type'] in ('submit', 'image') and not child.has_attr('name'):
          # Ignore submit/image with no name attribute
          continue
        if child['type'] in ('text', 'hidden', 'password', 'submit', 'image'):
            # Extract the <input> name attribute
            params.append(child['name'])
        injection_obj = ('POST', post_url, params, COOKIE)
        if injection_obj not in POST_INJECTION_OBJECTS:
          if injection_obj not in output:
            output.append(injection_obj)
  return output

def extract_get_fields(link, soup):
  output = []
  # Finds all href within the current page
  for a_element in soup.find_all('a', href=True):
    a_url = urlparse.urlparse(a_element['href'])
    # Extract list of params
    params = urlparse.parse_qs(a_url.query).keys()
    # Create full link then strip off the query params
    full_link = create_full_link(a_element['href'], link)
    full_link = full_link[:full_link.index("?")]
    injection_obj = ('GET', full_link, params, COOKIE)
    if injection_obj not in GET_INJECTION_OBJECTS:
      GET_INJECTION_OBJECTS.append(injection_obj)
      output.append(injection_obj)
  return output

def extract_injection_points(link, soup):
  post_urls = extract_post_fields(link, soup)
  get_urls = extract_get_fields(link, soup)
  post_urls.extend(get_urls)
  return post_urls

def make_json_results(results_lst):
  # Stub method
  # Creates the final results JSON needed for submission
  for result in results_lst:
    pass

def scan(link, soup):
  injection_obj_lst = extract_injection_points(link, soup)
  print("[*] Testing endpoint {}".format(link))
  sql_results = sql_injection_module.run(injection_obj_lst)
  return make_json_results([sql_results])

def test_vuln_modules(soup):
  sql_injection_module.run(soup)

def scan_stub(link, soup):
  # Temporary implementation of scan
  print(link)