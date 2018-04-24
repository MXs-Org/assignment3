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
  """Attempts to detect if there is a baseline present for the endpoint. Returns
  a list of possible baseline pages (aka error pages), or [""] if the <input> is
  echoed back in the response

  Args:
    injection_obj: tuple of (method, link, params, cookie)

  Returns:
    baseline_lst: a [String] of what the baseline response looks like. Returns [""]
    if no reasonable baseline can be determined i.e. <input> is echoed back to user
  """
  method, link, params, cookie = injection_obj
  # Test if response is different for Int and String
  # Int chosen such that it should be beyond the total number of rows in a DB
  # String chosen such that it should not reasonably be in present in DB
  # Mixed is for requests that start with an Int but contains characters
  int_payload = '111111'
  str_payload = 'quickbrownfoxlazydog'
  mixed_payload = int_payload + str_payload
  # Get the responses
  int_res = make_request(injection_obj, int_payload).content
  str_res = make_request(injection_obj, str_payload).content
  mixed_res = make_request(injection_obj, mixed_payload).content
  if int_res == str_res:
    # Means that error message is constant for both Int and String
    # Accept that response as a baseline
    return [int_res]
  if int_res != str_res:
    # Server handles Int and String inputs differently 
    if int_payload in int_res or str_payload in str_res:
      # Check if <input> is echoed back to the user
      return [""]
    else:
      if int_res == mixed_res:
        # Server parses the int and mixed the same way
        return [int_res, str_res]
      else:
        return [int_res, str_res, mixed_res]
  return [""]

def inject_payload(injection_obj, payload, baseline_lst):
  # import pdb; pdb.set_trace()
  method, link, params, cookie = injection_obj
  # if link == 'http://localhost:8888/openredirect/openredirect.php':
  #   import pdb; pdb.set_trace()
  res = make_request(injection_obj, payload)
  # Checks if the baseline_lst contains only a "", which means No Baseline
  if baseline_lst[0]:
    # res.content must be different from ALL the baseline
    if all([res.content != baseline for baseline in baseline_lst]):
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
      payloads = open('payloads/sql_injection_payloads.txt').read().splitlines()
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