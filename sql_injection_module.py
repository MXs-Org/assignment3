import requests
from bs4 import BeautifulSoup

"""
Things to do:
1. Check if server is using MySQL or SQLite (is this needed? Or just bruteforce)
2. Have a way to diff the two web responses
3. Include logging - details about endpoints discovered and crawled (print for now)
4. Send network requests GET, POST
"""

base_url = "http://localhost:8888"

def make_results_obj(url, field, payload):
  # Makes the Python object that will eventually be turned into a JSON object
  endpoint = url[len(base_url):]
  obj = {
    "endpoint": endpoint,
    "params": {
      field: payload
    },
    "method": "POST"
  }
  return obj

def extract_post_fields(link, soup):
  # Finds all possible SQL injection points present on the page
  # Returns { post_url: [list of fields] }
  post_dct = {}
  field_lst = []
  for form in soup.find_all('form'):
    if form.get('method') == "POST":
      # Extract the URL that the <form> is POSTing to
      post_url = link if not form.get('action') else link+form.get('action')
      # Extract the injectable HTML elements present in the <form>
      for child in form.find_all(recursive=False):
        # Ignore submit/image with no name attribute
        if child['type'] in ('submit', 'image') and not child.has_attr('name'):
            continue
        if child['type'] in ('text', 'hidden', 'password', 'submit', 'image'):
            # Extract the <input> name attribute
            field_lst.append(child['name'])
  post_dct[link] = field_lst
  if post_dct:
    print("[*] Injection points found. Iterating payloads...")
  return post_dct

def find_baseline(url, field):
  # Follow a simple flowchart to see if a baseline file can be determined
  # Returns the baseline_file. "" if baseline does not exist

  # Send a request with long garbage string (lower the chances that the page 
  # originally contains our POST data)
  res1 = requests.post(url, data={field: 'b1946ac92492d2347c6235b4d2611184'}).content
  res2 = requests.post(url, data={field: '91fc14ad02afd60985bb8165bda320a6'}).content
  # If the input data does not affect the response, it means that whatever 
  # response we get is the baseline
  if res1 == res2:
    return res1
  else:
    # How to handle cases where they say "<input> cannot be found"
    # i.e. <input> is echoed back to the user
    if 'b1946ac92492d2347c6235b4d2611184' in res1:
      return ""

def inject_payload(url, field, payload, baseline):
  res = requests.post(url, data={field: payload})
  if baseline:
    if res.content != baseline:
      print("[*] Working payload found!")
      print(url, field, payload)
      return make_results_obj(url, field, payload)
  else:
    # TODO: this might be a fragile assumption!
    # Making the assumption that if the injection worked, the <input> will NOT 
    # be echoed back to the user
    if payload not in res.content:
      print("[*] Working payload found!")
      print(url, field, payload)
      return make_results_obj(url, field, payload)

def iterate_payloads(injection_points):
  results = []
  [(url, fields)] = injection_points.items()
  for field in fields:
    # Issue a baseline request e.g. non-SQL injection query with innocent payload
    baseline = find_baseline(url, field)
    # Loads the payloads and tests them against the endpoint
    payloads = open('payloads/Auth_Bypass.txt').readlines()
    for payload in payloads:
      result = inject_payload(url, field, payload, baseline)
      if result:
        results.append(result)
        break
  return results  

def run(link, soup):
  print("[*] Testing for SQL Injection")
  injection_points = extract_post_fields(link, soup)
  results = iterate_payloads(injection_points)
  return results